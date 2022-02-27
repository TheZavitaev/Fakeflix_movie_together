import logging
from typing import List

import backoff
from clickhouse_driver import Client, errors
from config import settings
from models.models import ViewedFrame

logger = logging.getLogger(__name__)

client = Client(
    host=settings.CLICKHOUSE_MAIN_HOST,
    alt_hosts=settings.clickhouse_alt_hosts_to_string,
)


@backoff.on_exception(
    wait_gen=backoff.expo,
    exception=errors.Error,
    max_tries=10,
)
def init_clickhouse_database():
    client.execute(
        "CREATE DATABASE IF NOT EXISTS analytics ON CLUSTER company_cluster",
    )

    client.execute(  # noqa: WPS462
        """
        CREATE TABLE IF NOT EXISTS analytics.regular_table ON CLUSTER company_cluster
            (
                user_id UUID,
                movie_id UUID,
                movie_timestamp Int64
            )
            Engine=MergeTree()
        ORDER BY user_id
        """,
    )


@backoff.on_exception(
    wait_gen=backoff.expo,
    exception=errors.Error,
    max_tries=10,
)
def insert_bulk(events: List[ViewedFrame]):
    try:  # noqa: WPS229
        data = [(event.user_id, event.movie_id, event.movie_timestamp) for event in events]

        client.execute(  # noqa: WPS462
            """
            INSERT INTO analytics.regular_table
                (
                            user_id,
                            movie_id,
                            movie_timestamp
                )
            VALUES
            """, data
        )
        return True

    except errors.Error as error:
        logger.error(f'An error occurred while loading {events=} into ClickHouse - {error=}')
        return False
