from uuid import UUID

from pydantic import BaseModel


class ViewedFrame(BaseModel):
    user_id: UUID
    movie_id: UUID
    movie_timestamp: int


class Event(BaseModel):
    some_payload: ViewedFrame
