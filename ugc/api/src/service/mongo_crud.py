from uuid import UUID

from bson import ObjectId
from pydantic import BaseModel
from pymongo.errors import DuplicateKeyError
from service.exceptions import ItemAlreadyExists, ItemNotFound


class MongoCrud:
    def __init__(self, collection):
        self.collection = collection

    async def add_item(self, model: BaseModel):
        data = model.dict(by_alias=True, exclude={'id'})
        try:
            result = await self.collection.insert_one(data)
        except DuplicateKeyError:  # noqa: WPS329
            raise ItemAlreadyExists
        return await self.collection.find_one({"_id": result.inserted_id})

    async def get_item(self, item_id: str, user_id: UUID):
        item = await self.collection.find_one({'_id': ObjectId(item_id), 'user_id': user_id})
        if not item:
            raise ItemNotFound
        return item

    async def get_list(self, **kwargs):
        return await self.collection.find(kwargs).to_list(length=100)

    async def delete(self, item_id: str, user_id: UUID):
        delete_result = await self.collection.delete_one({'_id': ObjectId(item_id), 'user_id': user_id})
        if delete_result.deleted_count == 0:
            raise ItemNotFound
