import logging
import uuid
from functools import lru_cache
from typing import List, Optional
from uuid import UUID

from fastapi import Depends
from sqlalchemy import select, insert, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncEngine

from movie_together.app.src.core.auth.models import CustomUser
from movie_together.app.src.db.postgres import get_pg_engine
from movie_together.app.src.models.db_models import Room, RoomUser
from movie_together.app.src.models.models import RoomUserTypeEnum, RoomModel, RoomUserModel
from movie_together.app.src.services.base import BaseService

logger = logging.getLogger(__name__)


class RoomService(BaseService):

    async def create_user_room(self, room_id: UUID, user_id: str, link: str, film_work_uuid: UUID):
        async with self.get_session() as session:
            try:
                async with session.begin():
                    session.add(Room(
                        id=room_id,
                        room_users=[RoomUser(user_uuid=user_id, user_type=RoomUserTypeEnum.owner.value)],
                        owner_uuid=user_id,
                        film_work_uuid=film_work_uuid,
                        link=link
                    )
                    )
            except IntegrityError as exc:
                logger.error(exc)
                return f'Room for user "{user_id}" already exist!'

    async def get_room(self, room_id: UUID, user: CustomUser) -> Optional[RoomModel]:
        async with self.db_connection.begin() as conn:
            room_user_type = await conn.execute(
                select(RoomUser.user_type).where(
                    RoomUser.room_uuid == str(room_id),
                    RoomUser.user_uuid == str(user.pk),
                ))
            existed_room_user_type = room_user_type.scalars().first()
            if not existed_room_user_type:
                return None

            room = await conn.execute(select(Room).where(RoomUser.room_uuid == str(room_id)))
            existed_room = room.mappings().fetchone()
            return RoomModel(**existed_room) if existed_room else None

    async def join(self, user: CustomUser, room_id: str) -> Optional[str]:
        async with self.db_connection.begin() as conn:
            room = await conn.execute(select(Room.owner_uuid).where(Room.id == room_id))
            room_owner = room.scalars().first()

            if not room_owner:
                return f'Room "{room_id}" does not exist!'

            if user.pk == room_owner:
                return f'You are the owner of the room "{room_id}"!'

            try:
                await conn.execute(
                    insert(RoomUser, {
                        RoomUser.room_uuid.key: room_id,
                        RoomUser.user_uuid.key: user.pk,
                        RoomUser.user_type: RoomUserTypeEnum.member.value
                    })
                )
            except IntegrityError as exc:
                logger.error(exc)
                return f'Room user "{user.pk}" already exist!'

    async def get_room_users(self, room_id: str) -> List[RoomUserModel]:
        async with self.db_connection.begin() as conn:
            results = await conn.execute(select(RoomUser).where(RoomUser.room_uuid == room_id))
            room_users = results.mappings().fetchall()
            return [RoomUserModel(**room_user) for room_user in room_users] if room_users else []

    async def disconnect_user(self, user: CustomUser, room_id: str):
        async with self.db_connection.begin() as conn:
            if await conn.execute(delete(RoomUser).where(
                    RoomUser.room_uuid == str(room_id),
                    RoomUser.user_uuid == str(user.pk),
            )):
                return True

            return f'User "{user.pk}" does not exist in the room "{room_id}"!'


@lru_cache()
def get_room_service(
        db_connection: AsyncEngine = Depends(get_pg_engine),
) -> RoomService:
    return RoomService(db_connection)
