from functools import lru_cache
from uuid import UUID

from core.config import settings
from db.mongodb import get_mongodb
from fastapi import Depends
from models.mongo_models import LikeModel
from service.base_crud_service import BaseCrudService


class LikeService(BaseCrudService):
    async def add(self, like: LikeModel) -> LikeModel:
        created_event = await self.crud.add_item(like)
        return LikeModel.parse_obj(created_event)

    async def get(self, user_id: UUID, like_id: str):
        item = await self.crud.get_item(like_id, user_id)
        return LikeModel.parse_obj(item)

    async def get_list(self, user_id: UUID):
        items = await self.crud.get_list(user_id=user_id)
        return [LikeModel.parse_obj(item) for item in items]

    async def delete(self, user_id: UUID, like_id: str):
        await self.crud.delete(like_id, user_id)


@lru_cache()
def get_like_service(mongo_db=Depends(get_mongodb)) -> LikeService:
    return LikeService(mongo_db, settings.MONGO_COLLECTION_LIKE)
