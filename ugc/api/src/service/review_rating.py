from functools import lru_cache
from uuid import UUID

from core.config import settings
from db.mongodb import get_mongodb
from fastapi import Depends
from models.mongo_models import ReviewRatingModel
from service.base_crud_service import BaseCrudService


class ReviewRatingService(BaseCrudService):
    async def add(self, review: ReviewRatingModel):
        created_event = await self.crud.add_item(review)
        return ReviewRatingModel.parse_obj(created_event)

    async def get(self, user_id: UUID, item_id: str):
        item = await self.crud.get_item(item_id, user_id)
        return ReviewRatingModel.parse_obj(item)

    async def get_list(self, user_id: UUID, review_id: str):
        items = await self.crud.get_list(user_id=user_id, review_id=review_id)
        return [ReviewRatingModel.parse_obj(item) for item in items]

    async def delete(self, user_id: UUID, item_id: str):
        await self.crud.delete(item_id, user_id)


@lru_cache()
def get_review_rating_service(mongo_db=Depends(get_mongodb)) -> ReviewRatingService:
    return ReviewRatingService(mongo_db, settings.MONGO_COLLECTION_REVIEW_RATING)
