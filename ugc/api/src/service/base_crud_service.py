from abc import ABC

from core.config import settings
from service.mongo_crud import MongoCrud


class BaseCrudService(ABC):
    def __init__(self, mongodb_client, collection_name: str):
        self.client = mongodb_client
        self.collection = self.client[settings.MONGO_DATABASE][collection_name]
        self.crud = MongoCrud(self.collection)
