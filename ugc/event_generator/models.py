import uuid

from pydantic.main import BaseModel


class Film(BaseModel):
    movie_id: str = str(uuid.uuid4())


class User:
    user_id: str = str(uuid.uuid4())


class Review(BaseModel):
    review_id: str = str(uuid.uuid4())
    user_id: str
    movie_id: str
    user_rating: int
    text: str


class FilmLike(BaseModel):
    user_id: str
    movie_id: str
    rating: str


class ReviewLike(BaseModel):
    user_id: str
    review_id: str
    rating: str


class Bookmark(BaseModel):
    user_id: str
    bid: str
    movie_id: str


class FilmView(BaseModel):
    movie_id: str
    user_id: str
    movie_timestamp: int
