import random
import string
import time
from dataclasses import dataclass
from typing import List

import progressbar
from clickhouse_driver import Client

client = Client(host='localhost')


@dataclass
class Item:
    user_id: str
    movie_id: str
    time_stamp: int


def generate_user_id() -> str:
    letters = string.digits
    return str(''.join(random.choice(letters) for _ in range(10)))


def generate_movie_id() -> str:
    letters = string.ascii_lowercase + string.ascii_uppercase + string.digits
    return 'tt' + ''.join(random.choice(letters) for _ in range(10))


def insert_bulk(items: List[Item]):
    data = [(item.user_id, item.movie_id, item.time_stamp) for item in items]

    client.execute(
        """
        INSERT INTO analytics.regular_table
            (
                        user_id,
                        movie_id,
                        viewed_frame
            )
        VALUES
        """, data
    )


def generate():
    num_of_users = 1000
    num_of_movies = 1000
    num_of_timestamps = 100
    timestamp_max_diff = 40

    users = [generate_user_id() for _ in range(num_of_users)]

    for _ in progressbar.progressbar(range(num_of_movies)):
        movie_id = generate_movie_id()

        items = []
        for user in users:
            time_stamp = 0
            for _ in range(num_of_timestamps):
                items.append(Item(user_id=user, movie_id=movie_id, time_stamp=time_stamp))
                time_stamp += random.randint(1, timestamp_max_diff)
        insert_bulk(items)


def init_clickhouse_database():
    client.execute(
        "CREATE DATABASE IF NOT EXISTS analytics ON CLUSTER company_cluster",
    )
    client.execute(
        """
        CREATE TABLE IF NOT EXISTS analytics.regular_table ON CLUSTER company_cluster
            (
                user_id String,
                movie_id String,
                viewed_frame Int32
            )
            Engine=MergeTree()
        ORDER BY user_id
        """,
    )


def fetch_data(movie_id):
    begin = time.time()
    client.execute(
        f"SELECT * FROM analytics.regular_table where movie_id = '{movie_id}' ORDER BY user_id DESC, viewed_frame ASC"
    )
    print(f'Time: {time.time() - begin}')


def main():
    init_clickhouse_database()
    generate()
    fetch_data('ttFBFlPEcry0')


if __name__ == "__main__":
    main()
