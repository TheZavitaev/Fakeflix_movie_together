from random import randint

import orjson


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


def create_room_link() -> str:
    return f'https:://this_is_link_{randint(1, 999999)}'
