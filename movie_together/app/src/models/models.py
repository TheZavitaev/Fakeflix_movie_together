from datetime import datetime
from enum import Enum
from typing import List, Optional
from uuid import UUID

import orjson
from pydantic import BaseModel as PydanticBaseModel

from movie_together.app.src.core.utils import orjson_dumps


class RoomUserTypeEnum(str, Enum):
    member = 'member'
    owner = 'owner'


class BaseModel(PydanticBaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class ResponseModel(BaseModel):
    success: bool
    errors: List[str] = []
    link: str | None = None


class ResponseUser(BaseModel):
    success: bool
    errors: List[str] = []


class RoomModel(BaseModel):
    id: UUID
    owner_uuid: UUID
    film_work_uuid: Optional[UUID] = None


class RoomUserModel(BaseModel):
    id: Optional[UUID] = None
    room_uuid: UUID
    user_uuid: UUID
    created_at: datetime

    class Config:
        use_enum_values = True
