import json
import os

from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError


class Kafka:
    def __init__(self, servers_name=None, client_id='default_user'):

        if servers_name is None:
            servers_name = [f'{os.getenv("KAFKA_HOST", "kafka")}:{os.getenv("KAFKA_PORT", "29092")}', ]

        self.admin_client = KafkaAdminClient(bootstrap_servers=servers_name, client_id=client_id)

    def create_topic(self, topic_name=None, num_partitions=1, replication_factor=1):
        try:
            self.admin_client.create_topics(
                new_topics=[NewTopic(
                    name=topic_name,
                    num_partitions=num_partitions,
                    replication_factor=replication_factor
                )],
                validate_only=False
            )
            print(f'Topic "{topic_name}" successfully created!')
        except TopicAlreadyExistsError:
            print(f'Topic "{topic_name}" is already exist.')


if __name__ == '__main__':

    with open('./scripts/topics.json') as json_file:
        topics = json.load(json_file)

    kafka = Kafka(client_id='user_initialize_topics')
    for topic in topics:
        kafka.create_topic(topic_name=topic['name'])
