import logging
import sys

from aiokafka import AIOKafkaConsumer

# Initialize logger
from kafka import TopicPartition
from kafka.errors import KafkaError

from core.config import settings

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)


class KafkaConsumer:
    def __init__(
            self,
            config,
            kafka_min_commit_count=1,
            max_bulk_messages=10,
            max_timeout=5,
    ):
        self.config = config
        self.kafka_min_commit_count = kafka_min_commit_count
        self.max_bulk_messages = max_bulk_messages
        self.max_timeout = max_timeout

        self.consumer = AIOKafkaConsumer(
            bootstrap_servers=self.config.get('bootstrap_servers'),
            enable_auto_commit=self.config.get('enable_auto_commit'),
            auto_offset_reset=self.config.get('auto_offset_reset'),
        )

    def subscribe(self, topics: list[str]):
        self.consumer.subscribe(topics)

    def assign(self, partitions: list[tuple[str, int]]):
        partitions = [TopicPartition(topic, partition) for topic, partition in partitions]
        self.consumer.assign(partitions)

    async def start(self):
        await self.consumer.start()

    def raise_on_error(self, msg):
        # TODO отдебажить и поправить ошибки здесь
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                # End of partition event
                sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
                                 (msg.topic(), msg.partition(), msg.offset()))
            elif msg.error():
                raise KafkaError(msg.error())

            return True
        return False

    # TODO отдебажить msg, мб прикрутить сериализацию по нашей модели сообщения
    async def consume_loop(self, msg_process, *args, **kwargs):
        msg_bulk = []
        msg_count = 0
        async for msg in self.consumer:
            if msg is None:
                continue
            if self.raise_on_error(msg):
                continue

            logging.info(f'Received message from topic "{msg.topic()}"')

            msg_count += 1
            msg_bulk.append(msg)

            if len(msg_bulk) >= self.max_bulk_messages:
                await msg_process(msg_bulk, *args, **kwargs)
                msg_bulk = []
                if msg_count % self.kafka_min_commit_count == 0:
                    await self.consumer.commit()

    async def close(self):
        await self.consumer.stop()


def get_kafka_consumer() -> KafkaConsumer:
    return KafkaConsumer(config=settings.kafka_config)
