import json

from aiokafka import AIOKafkaProducer

from core.config import settings
from models.models import WebsocketMessage


def serializer(value):
    return json.dumps(value).encode('utf-8')


class KafkaProducer:
    def __init__(
            self,
            config=settings.kafka_config,
    ):
        self.config = config

        self.producer = AIOKafkaProducer(
            bootstrap_servers=self.config.get('bootstrap_servers'),
            key_serializer=serializer,
            value_serializer=serializer,
        )

    async def start(self):
        await self.producer.start()

    async def produce(self, topic_name: str, key: str, data):
        return await self.producer.send_and_wait(
            topic=topic_name,
            value=data,
            key=key,
        )

    async def close(self):
        await self.producer.stop()
