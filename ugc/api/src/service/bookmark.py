from functools import lru_cache
from uuid import UUID

from core.config import settings
from db.mongodb import get_mongodb
from fastapi import Depends
from models.mongo_models import BookmarkModel
from service.base_crud_service import BaseCrudService


class BookmarkService(BaseCrudService):
    async def add_bookmark(self, movie_id: UUID, user_id: UUID):
        bookmark = BookmarkModel(movie_id=movie_id, user_id=user_id)
        created_event = await self.crud.add_item(bookmark)
        return BookmarkModel.parse_obj(created_event)

    async def get_bookmark(self, user_id: UUID, item_id: str):
        item = await self.crud.get_item(item_id, user_id)
        return BookmarkModel.parse_obj(item)

    async def get_list(self, user_id: UUID):
        items = await self.crud.get_list(user_id=user_id)
        return [BookmarkModel.parse_obj(item) for item in items]

    async def delete_bookmark(self, user_id: UUID, item_id: str):
        await self.crud.delete(item_id, user_id)


@lru_cache()
def get_bookmark_service(mongo_db=Depends(get_mongodb)) -> BookmarkService:
    return BookmarkService(mongo_db, settings.MONGO_COLLECTION_BOOKMARK)
