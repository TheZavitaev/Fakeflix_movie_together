from multiprocessing import Pool
from sys import stdout

import tqdm
from pymongo import MongoClient

from bench.mongo.src.fake_gen import generate_user_documents, generate_movie_and_related_documents, movie_ids
from bench.mongo.src.config import settings


def upload_users_documents():
    client = MongoClient(settings.MONGO_HOST, settings.MONGO_PORT)
    db = client.get_database(settings.DB_NAME)

    collection = db.get_collection('users')
    collection.insert_many(generate_user_documents(), ordered=False)


def upload_movie_ratings_and_reviews(movie_id):
    client = MongoClient(settings.MONGO_HOST, settings.MONGO_PORT)
    db = client.get_database(settings.DB_NAME)

    movie, ratings, reviews = generate_movie_and_related_documents(movie_id)

    movies_coll = db.get_collection('movies')
    movies_coll.insert_one(movie)

    if ratings:
        ratings_coll = db.get_collection('movie_ratings')
        ratings_coll.insert_many(ratings, ordered=False)

    if reviews:
        reviews_coll = db.get_collection('reviews')
        reviews_coll.insert_many(reviews, ordered=False)

    client.close()


if __name__ == '__main__':
    stdout.write('гружу данные в монгу')
    upload_users_documents()
    stdout.write('готово!')

    stdout.write('загружаю ревью,фильмы и рейтинги')
    with Pool() as pool:
        r = list(tqdm.tqdm(
            pool.imap(upload_movie_ratings_and_reviews, movie_ids),
            total=len(movie_ids)
        ))
    stdout.write('готово!')
