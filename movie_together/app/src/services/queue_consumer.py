import json

from aiokafka import AIOKafkaConsumer
from core.config import settings
# Initialize logger
from kafka import TopicPartition


def deserializer(value):
    return json.loads(value.decode("utf-8"))


class KafkaConsumer:
    def __init__(
            self,
            config=settings.kafka_config,
            group_id=None,
            kafka_min_commit_count=5,
            max_bulk_messages=1,
            max_timeout=5,
    ):
        self.config = config
        self.group_id = str(group_id)
        self.kafka_min_commit_count = kafka_min_commit_count
        self.max_bulk_messages = max_bulk_messages
        self.max_timeout = max_timeout

        self.consumer = AIOKafkaConsumer(
            bootstrap_servers=self.config.get('bootstrap_servers'),
            enable_auto_commit=self.config.get('enable_auto_commit'),
            auto_offset_reset=self.config.get('auto_offset_reset'),
            group_id=self.group_id,
            key_deserializer=deserializer,
            value_deserializer=deserializer,
        )

    def subscribe(self, topics: list[str]):
        self.consumer.subscribe(topics)

    def assign(self, partitions: list[tuple[str, int]]):
        partitions = [TopicPartition(topic, partition) for topic, partition in partitions]
        self.consumer.assign(partitions)

    async def start(self):
        await self.consumer.start()

    async def consume_loop(self, msg_process, *args, **kwargs):
        msg_bulk = []
        msg_count = 0
        async for msg in self.consumer:
            msg_count += 1
            msg_bulk.append(msg)

            if len(msg_bulk) >= self.max_bulk_messages:
                await msg_process(
                        [msg.value for msg in msg_bulk],
                        *args,
                        **kwargs
                    )
                msg_bulk = []
                if msg_count % self.kafka_min_commit_count == 0:
                    await self.consumer.commit()
                    msg_count = 0

    async def close(self):
        await self.consumer.stop()
