import time
from datetime import datetime
from enum import Enum
from typing import Any, List, Optional, Union
from uuid import UUID

import orjson
from pydantic import BaseModel as PydanticBaseModel

from core.utils import orjson_dumps


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
    link: Optional[str] = None


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


class User(BaseModel):
    username: str
    first_name: str
    last_name: str
    id: UUID


class MessageAction(str, Enum):
    connect = 'CONNECT'
    disconnect = 'DISCONNECT'
    message = 'MESSAGE'
    player_timeupdate = 'PLAYER-timeupdate'
    player_play = 'PLAYER-play'
    player_pause = 'PLAYER-pause'


class WebsocketMessage(BaseModel):
    action: MessageAction
    data: Union[dict, str]
    username: Optional[str] = None
    datetime: Optional[int] = None
    room_id: Optional[UUID] = None
    connect_id: Optional[UUID] = None

    def __init__(self, **data: Any):
        super().__init__(**data)
        self.datetime = data.get('datetime', int(time.time()))

