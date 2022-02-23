from typing import List

from pydantic import BaseSettings


class Settings(BaseSettings):
    # kafka
    KAFKA_TOPIC: str = 'movie_progress'
    KAFKA_HOST: str = 'kafka:9092'
    KAFKA_CONSUMER_GROUP: str = 'ETL_Kafka_to_ClickHouse'

    # clickhouse
    CLICKHOUSE_MAIN_HOST: str = 'clickhouse-node1'
    CLICKHOUSE_ALT_HOSTS: List[str] = ['clickhouse-node2', 'clickhouse-node3', 'clickhouse-node4']

    # ETL
    OFFSET: int = 100
    SLEEP_TIME: int = 5

    @property
    def clickhouse_alt_hosts_to_string(self):
        return ','.join(self.CLICKHOUSE_ALT_HOSTS)


settings = Settings()
