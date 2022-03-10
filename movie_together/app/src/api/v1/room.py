import asyncio
import json
import os
import uuid
from typing import Optional

import aiohttp
from core.auth.decorators import login_required
from core.config import settings
from core.utils import create_room_link, create_short_link
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, status
from models.models import (MessageAction, ResponseModel, ResponseUser, User,
                           WebsocketMessage)
from services.queue_consumer import KafkaConsumer
from services.queue_producer import KafkaProducer
from services.room import RoomService, get_room_service
from starlette.requests import Request

room_router = APIRouter()


@room_router.post('/', response_model=ResponseModel)
@login_required()
async def create_room(
        request: Request,
        service: RoomService = Depends(get_room_service),
) -> ResponseModel:

    room_id = uuid.uuid4()
    film_work_uuid = uuid.uuid4()

    error = await service.create_user_room(
        room_id=room_id,
        user_id=request.user.pk,
        link=create_room_link(room_id),
        film_work_uuid=film_work_uuid
    )
    if error:
        return ResponseModel(success=False, errors=[error])
    link = create_short_link(create_room_link(room_id))
    return ResponseModel(success=True, link=create_room_link(room_id))


@room_router.post('/{room_id}/disconnect', response_model=ResponseUser)
@login_required()
async def disconnect_user(
        request: Request,
        room_id: str,
        service: RoomService = Depends(get_room_service)
) -> ResponseUser:

    result = await service.disconnect_user(user=request.user, room_id=room_id)

    if not result:
        return ResponseUser(success=False)

    return ResponseUser(success=True)


@room_router.get('/{room_id}/join', response_model=ResponseUser)
@login_required()
async def join_user(
        request: Request,
        room_id: str,
        service: RoomService = Depends(get_room_service)
) -> ResponseUser:

    error = await service.join(user=request.user, room_id=room_id)

    if error:
        return ResponseUser(success=False, errors=[error])

    return ResponseUser(success=True)


async def send_to_websocket(
        messages: list,
        websocket: WebSocket,
        current_session: uuid.UUID,
        current_connect: uuid.UUID
):
    for message in messages:
        message_obj = WebsocketMessage(**json.loads(message))
        if message_obj.room_id == current_session and message_obj.connect_id != current_connect:
            del message_obj.connect_id
            await websocket.send_text(message_obj.json())


async def get_user_data(authorization: str) -> Optional[User]:
    async with aiohttp.ClientSession() as session:
        resp = await session.get(
            url=os.path.join(
                settings.auth_service_url,
                settings.AUTH_SERVICE_API_ENDPOINT,
                settings.AUTH_SERVICE_V1_ENDPOINT,
                settings.AUTH_SERVICE_GET_ME_ENDPOINT,
            ),
            headers={
                settings.AUTHORIZATION_HEADER_NAME: authorization,
            },
        )
        if resp.status != 201:
            return
        raw_user = await resp.json()
        return User(**raw_user)


@room_router.websocket('/{room_id}')
async def websocket_endpoint(
        websocket: WebSocket,
        room_id: str,
        auth: str = '',
        room_service: RoomService = Depends(get_room_service),
):
    room_id_as_uuid = uuid.UUID(room_id)

    await websocket.accept()
    user = await get_user_data(auth)
    if not user:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    connect_id = uuid.uuid4()

    room_users = await room_service.get_room_users(room_id)
    for room_user in room_users:
        if room_user.user_uuid == user.id:
            break
    else:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    consumer = KafkaConsumer(group_id=connect_id)
    producer = KafkaProducer()
    await consumer.start()
    await producer.start()

    result = await producer.produce(
        settings.KAFKA_TOPIC,
        room_id,
        WebsocketMessage(
            action=MessageAction.connect,
            room_id=room_id_as_uuid,
            username=user.username,
            connect_id=connect_id,
            data=user,
        ).json(),
    )
    consumer.assign([(settings.KAFKA_TOPIC, result.partition)])

    loop = asyncio.get_event_loop()
    task = loop.create_task(consumer.consume_loop(send_to_websocket, websocket, room_id_as_uuid, connect_id))

    try:
        while True:
            message_raw = await websocket.receive_json()
            message = WebsocketMessage(**message_raw)
            message.connect_id = connect_id
            message.username = user.username
            message.room_id = room_id_as_uuid
            await producer.produce(settings.KAFKA_TOPIC, room_id, message.json())
    except WebSocketDisconnect:
        await producer.produce(
            settings.KAFKA_TOPIC,
            room_id,
            WebsocketMessage(
                action=MessageAction.disconnect,
                room_id=room_id_as_uuid,
                username=user.username,
                connect_id=connect_id,
                data=user,
            ).json(),
        )
        task.cancel()
        await producer.close()
        await consumer.close()
