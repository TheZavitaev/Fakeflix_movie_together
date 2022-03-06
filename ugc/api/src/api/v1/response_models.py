from enum import Enum
from uuid import UUID

from models.mongo_models import LikeModel, ReviewRatingModel
from pydantic import BaseModel


class RatingLike(Enum):
    DISLIKE = 'DISLIKE'
    LIKE = "LIKE"


class RatingAddModel(BaseModel):
    rating: RatingLike
    movie_id: UUID


class RatingGetModel(BaseModel):
    id: str
    user_id: UUID
    movie_id: UUID
    rating: RatingLike

    @classmethod
    def from_service_model(cls, model: LikeModel):
        return cls(
            id=str(model.id),
            user_id=model.user_id,
            movie_id=model.movie_id,
            rating=RatingLike.LIKE if model.rating == LikeModel.get_max_rating() else RatingLike.DISLIKE
        )


class BookmarkGetModel(BaseModel):
    id: str
    user_id: UUID
    movie_id: UUID

    @classmethod
    def from_service_model(cls, model):
        return cls(
            id=str(model.id),
            user_id=model.user_id,
            movie_id=model.movie_id,
        )


class BookmarkAddModel(BaseModel):
    movie_id: UUID


class ReviewAddModel(BaseModel):
    movie_id: UUID
    text: str
    user_rating: int


class ReviewGetModel(BaseModel):
    id: str
    user_id: UUID
    movie_id: UUID
    text: str
    user_rating: int

    @classmethod
    def from_service_model(cls, model):
        return cls(
            id=str(model.id),
            user_id=model.user_id,
            movie_id=model.movie_id,
            text=model.text,
            user_rating=model.user_rating
        )


class ReviewRatingAddModel(BaseModel):
    rating: RatingLike


class ReviewRatingGetModel(BaseModel):
    id: str
    review_id: str
    user_id: UUID
    rating: RatingLike

    @classmethod
    def from_service_model(cls, model: ReviewRatingModel):
        return cls(
            id=str(model.id),
            user_id=model.user_id,
            review_id=model.review_id,
            rating=RatingLike.LIKE if model.user_rating == ReviewRatingModel.get_max_rating() else RatingLike.DISLIKE
        )
