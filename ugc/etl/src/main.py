import json
from time import sleep

from config import settings
from kafka import KafkaConsumer
from models.models import ViewedFrame
from service.clickhouse import init_clickhouse_database, insert_bulk


def consume_loop(cons: KafkaConsumer):
    try:  # noqa: WPS501
        while running:
            events: list[ViewedFrame] = []

            cons.poll()
            for message in cons:
                events.append(ViewedFrame(**message.value))

                if message.offset % settings.OFFSET == 0:
                    if insert_bulk(events):  # смещаем офсет и очищаем список, только если удалось записать в КХ
                        commit_offset(cons, events)  # noqa: WPS220
    finally:
        cons.close()


def commit_offset(cons: KafkaConsumer, events: list):
    cons.commit()
    events.clear()
    sleep(settings.SLEEP_TIME)


if __name__ == '__main__':
    running = True

    consumer = KafkaConsumer(
        settings.KAFKA_TOPIC,
        bootstrap_servers=settings.KAFKA_HOST,
        auto_offset_reset='smallest',
        value_deserializer=lambda msg: json.loads(msg),
        group_id=settings.KAFKA_CONSUMER_GROUP
    )

    init_clickhouse_database()
    consume_loop(consumer)
