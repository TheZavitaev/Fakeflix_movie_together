import typing
import uuid
from http import HTTPStatus

from api.v1.response_models import ReviewGetModel
from fastapi import APIRouter, Depends, Path, Query
from models.mongo_models import MovieLikes
from pydantic import BaseModel
from service.exceptions import ItemNotFound
from service.movie_likes import get_movie_likes_service, get_movie_reviews_service
from starlette.responses import JSONResponse

router = APIRouter()


class MovieLikesGetModel(BaseModel):
    likes: int
    dislikes: int

    @classmethod
    def from_service_model(cls, obj: MovieLikes):
        return cls(likes=obj.likes, dislikes=obj.dislikes)


@router.get(
    "/{movie_id}",
    summary="Получить количество лайков и дизлайков фильма",
    response_model=MovieLikesGetModel,
    tags=["Movies"],
)
async def movie_likes(
    movie_id: uuid.UUID = Path(..., title="Movie ID"),
    movie_likes_service=Depends(get_movie_likes_service),
) -> typing.Union[MovieLikesGetModel, JSONResponse]:
    try:
        likes_data = await movie_likes_service.get(movie_id)
    except ItemNotFound:
        return JSONResponse(status_code=HTTPStatus.NOT_FOUND, content={"message": "Item not found"})
    return MovieLikesGetModel.from_service_model(likes_data)


@router.get(
    "/{movie_id}/reviews/",
    summary="Список рецензий фильма",
    response_model=list[ReviewGetModel]
)
async def movie_reviews(
        movie_id: uuid.UUID = Path(..., title="Movie ID"),
        review_service=Depends(get_movie_reviews_service),
        page: int = Query(1, ge=1),
        sort: str = Query(1, regex="-?1")
) -> list[ReviewGetModel]:
    items = await review_service.get_list(movie_id, page, int(sort))
    return [ReviewGetModel.from_service_model(item) for item in items]
