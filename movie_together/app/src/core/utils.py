from uuid import UUID

import orjson
import pyshorteners as sh

from core.config import settings


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


def create_room_link(room_id: UUID):
    return f'{settings.get_root_url}/api/v1/room/{str(room_id)}/join'


def create_short_link(url) -> str:
    s = sh.Shortener()
    return s.tinyurl.short(url)
