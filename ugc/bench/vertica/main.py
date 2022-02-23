import argparse
import random
import string
import sys
import time
from dataclasses import dataclass
from typing import List

import progressbar
import vertica_python

connection_info = {
    'host': '127.0.0.1',
    'port': 5433,
    'user': 'dbadmin',
    'password': '',
    'database': 'docker',
    'autocommit': True,
}


@dataclass
class Item:
    user_id: int
    movie_id: str
    timestamp: int


class VerticaBencher:
    @staticmethod
    def create_table():
        with vertica_python.connect(**connection_info) as connection:
            cursor = connection.cursor()
            cursor.execute("""
            CREATE TABLE views (
                id IDENTITY,
                user_id INTEGER NOT NULL,
                movie_id VARCHAR(256) NOT NULL,
                viewed_frame INTEGER NOT NULL
            );
            """)

    @staticmethod
    def _insert(user_id, movie_id, timestamp):
        with vertica_python.connect(**connection_info) as connection:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO views (user_id, movie_id, viewed_frame) VALUES (%s, %s, %s);",
                (user_id, movie_id, timestamp)
            )

    @staticmethod
    def _insert_bulk(items: List[Item]):
        data = [(item.user_id, item.movie_id, item.timestamp) for item in items]

        with vertica_python.connect(**connection_info) as connection:
            cursor = connection.cursor()
            cursor.executemany(
                "INSERT INTO views (user_id, movie_id, viewed_frame) VALUES (%s, %s, %s);",
                data
            )

    @staticmethod
    def fetch_data(movie_id):
        with vertica_python.connect(**connection_info) as connection:
            cursor = connection.cursor()

            begin = time.time()
            cursor.execute(
                "SELECT * FROM views where movie_id = %s ORDER BY user_id DESC, viewed_frame ASC;",
                (movie_id,)
            )
            records = cursor.fetchall()
            print(f'Num of entries fetched: {len(records)}')
            print(f'Time: {time.time() - begin}')

    @staticmethod
    def _generate_user_id() -> int:
        letters = string.digits
        return int(''.join(random.choice(letters) for i in range(10)))

    @staticmethod
    def _generate_movie_id() -> str:
        letters = string.ascii_lowercase + string.ascii_uppercase + string.digits
        return 'tt' + ''.join(random.choice(letters) for i in range(10))

    @staticmethod
    def generate():
        num_of_users = 1000
        num_of_movies = 1000
        num_of_timestamps = 100
        timestamp_max_diff = 40

        users = [VerticaBencher._generate_user_id() for _ in range(num_of_users)]

        for _ in progressbar.progressbar(range(num_of_movies)):
            movie_id = VerticaBencher._generate_movie_id()

            items = []
            for user in users:
                timestamp = 0
                for _ in range(num_of_timestamps):
                    items.append(Item(user_id=user, movie_id=movie_id, timestamp=timestamp))
                    timestamp += random.randint(1, timestamp_max_diff)

            VerticaBencher._insert_bulk(items)


def main():
    parser = argparse.ArgumentParser(description='Vertica bench utility')
    parser.add_argument('command', choices=["create", "generate", "bench"], type=str,
                        help='Utility commands')
    parser.add_argument('--movie_id', type=str, required='bench' in sys.argv, help='Movie id to fetch')
    args = parser.parse_args()

    if args.command == 'create':
        VerticaBencher.create_table()
    elif args.command == 'generate':
        VerticaBencher.generate()
    if args.command == 'bench':
        VerticaBencher.fetch_data(args.movie_id)


if __name__ == "__main__":
    main()
