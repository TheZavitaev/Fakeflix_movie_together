from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from starlette.background import BackgroundTasks
from starlette.requests import Request

from core.config import settings
from movie_together.app.src.core.auth.decorators import login_required
from movie_together.app.src.models.models import ResponseModel
from movie_together.app.src.services.room import RoomService, get_room_service
from services.queue_consumer import KafkaConsumer, get_kafka_consumer
from services.queue_producer import KafkaProducer, get_kafka_producer

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


async def send_to_websocket(messages: list, websocket: WebSocket):
    for message in messages:
        await websocket.send_json(message)


@room_router.websocket('/{session_num}')
# @login_required()
async def websocket_endpoint(
        websocket: WebSocket,
        session_num: int,
        background_tasks: BackgroundTasks,
        consumer: KafkaConsumer = Depends(get_kafka_consumer),
        producer: KafkaProducer = Depends(get_kafka_producer),
):
    # TODO проверять, состоит ли данный пользователь в группе
    await consumer.start()
    await producer.start()

    # TODO send connect message to queue
    try:
        consumer.assign([(settings.KAFKA_TOPIC, session_num)])
        background_tasks.add_task(consumer.consume_loop, send_to_websocket)

        while True:
            message = await websocket.receive_json()
            await producer.produce(settings.KAFKA_TOPIC, session_num, message)
    except WebSocketDisconnect:
        pass
        # TODO send disconnect message to queue
        # TODO disconnect from queue
    finally:
        await producer.close()
        await consumer.close()
