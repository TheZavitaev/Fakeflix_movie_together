import asyncio
import uuid

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, Header
from starlette.background import BackgroundTasks
from starlette.requests import Request

from core.config import settings
from movie_together.app.src.core.auth.decorators import login_required
from movie_together.app.src.models.models import ResponseModel
from movie_together.app.src.services.room import RoomService, get_room_service
from services.queue_consumer import KafkaConsumer
from services.queue_producer import KafkaProducer

room_router = APIRouter()


# @room_router.post('/', response_model=ResponseModel)
# @login_required()
# async def create_room(
#         request: Request,
#         service: RoomService = Depends(get_room_service),
# ) -> ResponseModel:
#     error = await service.create_user_room(user_id=request.user.pk)
#     if error:
#         return ResponseModel(success=False, errors=[error])
#     return ResponseModel(success=True)


async def send_to_websocket(messages: list, websocket: WebSocket, current_session: str, current_connect: str):
    for message in messages:
        if message.get('session_id') == current_session and message.get('connect_id') != current_connect:
            await websocket.send_json(message)


# TODO сериализация сообщения
@room_router.websocket('/{session_id}')
async def websocket_endpoint(
        websocket: WebSocket,
        session_id: str,
        user: str = Header(None)
):
    await websocket.accept()
    # TODO получать id подключения, чтобы создавать group_id
    connect_id = str(uuid.uuid4())
    # TODO получать id пользователя из auth по bearer-токену
    user_id = user
    # TODO проверять, состоит ли данный пользователь в комнате

    consumer = KafkaConsumer(group_id=connect_id)
    producer = KafkaProducer()
    await consumer.start()
    await producer.start()

    result = await producer.produce_json(
        settings.KAFKA_TOPIC,
        session_id,
        {"action": "CONNECT", "session_id": session_id, "user_id": user_id, "connect_id": connect_id}
    )
    consumer.assign([(settings.KAFKA_TOPIC, result.partition)])

    loop = asyncio.get_event_loop()
    task = loop.create_task(consumer.consume_loop(send_to_websocket, websocket, session_id, connect_id))

    try:
        while True:
            message = await websocket.receive_json()
            message["connect_id"] = connect_id
            message["user_id"] = user_id
            message["session_id"] = session_id
            await producer.produce_json(settings.KAFKA_TOPIC, session_id, message)
    except WebSocketDisconnect:
        await producer.produce_json(
            settings.KAFKA_TOPIC,
            session_id,
            {"action": "DISCONNECT", "session_id": session_id, "user_id": user_id, "connect_id": connect_id}
        )
        task.cancel()
        await producer.close()
        await consumer.close()
