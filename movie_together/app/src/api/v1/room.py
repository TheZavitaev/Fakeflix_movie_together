import time
from typing import Optional

import aiohttp
import aiohttp
import asyncio
import uuid

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, Header, status
from starlette.background import BackgroundTasks
from starlette.requests import Request

from movie_together.app.src.core.config import settings
from movie_together.app.src.core.auth.decorators import login_required
from movie_together.app.src.core.utils import create_short_link, create_room_link
from movie_together.app.src.models.models import ResponseModel, ResponseUser
from movie_together.app.src.services.room import RoomService, get_room_service
from movie_together.app.src.services.queue_consumer import KafkaConsumer
from movie_together.app.src.services.queue_producer import KafkaProducer

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
    return ResponseModel(success=True, link=link)


@room_router.post('/disconnect', response_model=ResponseUser)
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


@room_router.get('/join', response_model=ResponseUser)
@login_required()
async def join_user(
        request: Request,
        room_id: str,
        service: RoomService = Depends(get_room_service)
) -> ResponseUser:

    error = await service.join(user=request.user, room_id=room_id)

    if error:
        return ResponseUser(success=True, errors=[error])

    return ResponseUser(success=False)


# TODO сериализация сообщения

async def send_to_websocket(messages: list, websocket: WebSocket, current_session: str, current_connect: str):
    for message in messages:
        if message.get('room_id') == current_session and message.get('connect_id') != current_connect:
            del message['connect_id']
            await websocket.send_json(message)


# TODO return model instead of dict
async def get_user_data(authorization: str) -> Optional[dict]:
    async with aiohttp.ClientSession() as session:
        # TODO url and header name from config envs
        resp = await session.get(
            'http://localhost:5555/api/v1/me',
            headers={
                "authorization": authorization,
            },
        )
        if resp.status != 200:
            return
        return await resp.json()


@room_router.websocket('/{room_id}')
async def websocket_endpoint(
        websocket: WebSocket,
        room_id: str,
        auth: str = "",
):
    await websocket.accept()
    user = await get_user_data(auth)
    if not user:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    connect_id = str(uuid.uuid4())
    # TODO проверять, состоит ли данный пользователь в комнате

    consumer = KafkaConsumer(group_id=connect_id)
    producer = KafkaProducer()
    await consumer.start()
    await producer.start()

    result = await producer.produce_json(
        settings.KAFKA_TOPIC,
        room_id,
        {
            "action": "CONNECT",
            "room_id": room_id,
            "username": user["username"],
            "connect_id": connect_id,
            "data": user,
            "datetime": int(time.time()),
        }
    )
    consumer.assign([(settings.KAFKA_TOPIC, result.partition)])

    loop = asyncio.get_event_loop()
    task = loop.create_task(consumer.consume_loop(send_to_websocket, websocket, room_id, connect_id))

    try:
        while True:
            message = await websocket.receive_json()
            message["connect_id"] = connect_id
            message["username"] = user["username"]
            message["room_id"] = room_id
            message["datetime"] = int(time.time()),
            await producer.produce_json(settings.KAFKA_TOPIC, room_id, message)
    except WebSocketDisconnect:
        await producer.produce_json(
            settings.KAFKA_TOPIC,
            room_id,
            {
                "action": "DISCONNECT",
                "room_id": room_id,
                "username": user["username"],
                "connect_id": connect_id,
                "datetime": int(time.time()),
            }
        )
        task.cancel()
        await producer.close()
        await consumer.close()
