from functools import lru_cache

from motor.motor_asyncio import AsyncIOMotorClient

mongodb_engine: AsyncIOMotorClient = None


@lru_cache()
def get_mongodb():
    return mongodb_engine
