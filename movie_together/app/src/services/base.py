from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.orm import sessionmaker


class BaseService:
    def __init__(self, db_connection: AsyncEngine):
        self.db_connection = db_connection

    def get_session(self) -> AsyncSession:
        return sessionmaker(self.db_connection, expire_on_commit=False, class_=AsyncSession)()
