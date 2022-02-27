from aiokafka import AIOKafkaProducer

from core.config import settings


class KafkaProducer:
    def __init__(
            self,
            config,
    ):
        self.config = config

        self.producer = AIOKafkaProducer(
            bootstrap_servers=self.config.get('bootstrap_servers'),
        )

    async def start(self):
        await self.producer.start()

    # TODO encode message
    async def produce(self, topic_name: str, partition: int, msg):
        await self.producer.send_and_wait(topic_name, msg, partition=partition)

    async def close(self):
        await self.producer.stop()


def get_kafka_producer() -> KafkaProducer:
    return KafkaProducer(config=settings.kafka_config)
