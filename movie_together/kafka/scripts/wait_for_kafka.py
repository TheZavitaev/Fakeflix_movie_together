import os
import time

from kafka import KafkaAdminClient
from kafka.errors import NoBrokersAvailable, NodeNotReadyError


def main():
    servers_name = [f'{os.getenv("KAFKA_HOST", "kafka")}:{os.getenv("KAFKA_PORT", "29092")}', ]
    print('Connecting to Kafka...')
    while True:
        try:
            client = KafkaAdminClient(
                bootstrap_servers=servers_name,
                client_id='default_user'
            )
            if client:
                print('Connected')
                exit()
        except (NoBrokersAvailable, NodeNotReadyError):
            print("Can't connect to Kafka on host %s", servers_name)
            time.sleep(3)


if __name__ == '__main__':
    main()
