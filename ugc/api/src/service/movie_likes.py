import uuid
from functools import lru_cache

from core.config import settings
from db.mongodb import get_mongodb
from fastapi import Depends
from models.mongo_models import MovieLikes, ReviewModel
from motor.motor_asyncio import AsyncIOMotorClient
from service.exceptions import ItemNotFound


class MongoService:
    def __init__(self, client: AsyncIOMotorClient, collection: str):
        self.client = client
        self.collection = self.client[settings.MONGO_DATABASE][collection]


class MovieLikesService(MongoService):
    async def get(self, movie_id: uuid.UUID) -> MovieLikes:
        movie_likes = await self.collection.find_one({"movie_id": str(movie_id)})
        if not movie_likes:
            raise ItemNotFound
        return MovieLikes.parse_obj(movie_likes)


@lru_cache
def get_movie_likes_service(mongo_db=Depends(get_mongodb)) -> MovieLikesService:
    return MovieLikesService(mongo_db, settings.MONGO_COLLECTION_MOVIES)


class ReviewService(MongoService):
    async def get_list(self, movie_id: uuid.UUID, page: int, sort: int) -> list[ReviewModel]:
        items = (
            await self.collection.find({"movie_id": str(movie_id)})
            .skip((page - 1) * settings.PAGE_SIZE)
            .limit(settings.PAGE_SIZE)
            .sort("user_rating", sort)
            .to_list(settings.PAGE_SIZE)
        )
        return [ReviewModel.parse_obj(item) for item in items]


@lru_cache
def get_movie_reviews_service(mongo_db=Depends(get_mongodb)) -> ReviewService:
    return ReviewService(mongo_db, settings.MONGO_COLLECTION_REVIEW)
