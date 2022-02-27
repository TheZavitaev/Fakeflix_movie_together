from uuid import UUID

from bson.objectid import ObjectId
from pydantic import BaseModel, Field


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value):
        if not ObjectId.is_valid(value):
            raise ValueError("Invalid objectid")
        return ObjectId(value)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class LikeModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    movie_id: UUID
    user_id: UUID
    rating: int

    @staticmethod
    def get_min_rating():
        return 0

    @staticmethod
    def get_max_rating():
        return 10

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class BookmarkModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    movie_id: UUID
    user_id: UUID

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class ReviewModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    movie_id: UUID
    user_id: UUID
    text: str
    user_rating: int

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class ReviewRatingModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    review_id: str
    user_id: UUID
    user_rating: int

    @staticmethod
    def get_min_rating():
        return 0

    @staticmethod
    def get_max_rating():
        return 10

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class MovieLikes(BaseModel):
    movie_id: UUID
    likes: int
    dislikes: int

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
