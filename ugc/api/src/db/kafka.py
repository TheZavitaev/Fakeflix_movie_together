import asyncio
import logging
from abc import ABC, abstractmethod

from aiokafka import AIOKafkaProducer
from core.config import settings
from core.exceptions import InsertEventTimeout
from kafka.errors import KafkaTimeoutError

logger = logging.getLogger(__name__)


class AbstractKafkaProducer(ABC):
    def __init__(self, kafka_server: str):
        self.kafka_server = kafka_server

    @abstractmethod
    async def start_producer(self):
        pass

    @abstractmethod
    async def stop_producer(self):
        pass

    @abstractmethod
    async def send(self, topic: str, key: str, value: str):
        pass


class AsyncKafkaProducer(AbstractKafkaProducer):

    def __init__(self, kafka_server: str):
        super().__init__(kafka_server)
        loop = asyncio.get_event_loop()
        self.producer = AIOKafkaProducer(
            loop=loop,
            client_id=settings.PROJECT_NAME,
            bootstrap_servers=self.kafka_server,
        )

    async def start_producer(self):
        await self.producer.start()

    async def stop_producer(self):
        await self.producer.stop()

    async def send(self, topic: str, key: str, value: str):
        data = value.encode('UTF-8')
        key = key.encode('UTF-8')  # type: ignore

        try:
            await self.producer.send_and_wait(topic=topic, key=key, value=data)
        except KafkaTimeoutError:
            raise InsertEventTimeout('Error send event')


kafka_producer: AbstractKafkaProducer = None  # type: ignore


async def get_kafka_producer() -> AbstractKafkaProducer:
    return kafka_producer
