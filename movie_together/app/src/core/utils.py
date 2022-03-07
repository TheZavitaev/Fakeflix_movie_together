from uuid import UUID

import orjson
import pyshorteners as sh


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


def create_room_link(room_id: UUID):
    return f'http://0.0.0.0:8000/api/v1/room/join?room_id={str(room_id)}'


def create_short_link(url) -> str:
    s = sh.Shortener()
    return s.tinyurl.short(url)
