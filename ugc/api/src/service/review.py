from functools import lru_cache
from uuid import UUID

from core.config import settings
from db.mongodb import get_mongodb
from fastapi import Depends
from models.mongo_models import ReviewModel
from service.base_crud_service import BaseCrudService


class ReviewService(BaseCrudService):
    async def add(self, movie_id: UUID, user_id: UUID, text: str, user_rating: int):
        review = ReviewModel(movie_id=movie_id, user_id=user_id, text=text, user_rating=user_rating)
        created_event = await self.crud.add_item(review)
        return ReviewModel.parse_obj(created_event)

    async def get(self, user_id: UUID, review_id: str):
        item = await self.crud.get_item(review_id, user_id)
        return ReviewModel.parse_obj(item)

    async def get_list_by_user(self, user_id: UUID):
        items = await self.crud.get_list(user_id=user_id)
        return [ReviewModel.parse_obj(item) for item in items]

    async def delete(self, user_id: UUID, review_id: str):
        await self.crud.delete(review_id, user_id)


@lru_cache()
def get_review_service(mongo_db=Depends(get_mongodb)) -> ReviewService:
    return ReviewService(mongo_db, settings.MONGO_COLLECTION_REVIEW)
