from http import HTTPStatus
from typing import List
from uuid import UUID

from api.v1 import response_models
from core.jwt_user_verify import JwtUserVerify
from fastapi import APIRouter, Depends, HTTPException, Path
from fastapi.security import OAuth2PasswordBearer
from models.mongo_models import LikeModel, ReviewRatingModel
from service.bookmark import get_bookmark_service
from service.exceptions import ItemAlreadyExists, ItemNotFound
from service.like import get_like_service
from service.review import get_review_service
from service.review_rating import get_review_rating_service

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

jwt_user_verify = JwtUserVerify()


@router.get(
    "/{user_id}/ratings/",
    summary="Получить все оценки пользователя",
    response_model=List[response_models.RatingGetModel],
    tags=["Likes"],
    dependencies=[Depends(jwt_user_verify)],
)
async def rating_list(
    user_id: UUID = Path(..., title="User ID"), like_service=Depends(get_like_service)
) -> List[response_models.RatingGetModel]:
    items = await like_service.get_list(user_id)
    return [response_models.RatingGetModel.from_service_model(item) for item in items]


@router.get(
    "/{user_id}/ratings/{rating_id}",
    summary="Получить оценку пользователя по ID",
    response_model=response_models.RatingGetModel,
    tags=["Likes"],
    dependencies=[Depends(jwt_user_verify)],
)
async def rating_get_by_id(
    user_id: UUID = Path(..., title="User ID"),
    rating_id: str = Path(..., title="Rating ID"),
    like_service=Depends(get_like_service),
) -> response_models.RatingGetModel:
    try:
        item = await like_service.get(user_id, rating_id)
    except ItemNotFound:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    return response_models.RatingGetModel.from_service_model(item)


@router.post(
    "/{user_id}/ratings",
    summary="Добавить оценку фильма",
    response_model=response_models.RatingGetModel,
    tags=["Likes"],
    dependencies=[Depends(jwt_user_verify)],
)
async def rating_add(
    data: response_models.RatingAddModel,
    user_id: UUID = Path(..., title="User ID"),
    like_service=Depends(get_like_service),
) -> response_models.RatingGetModel:
    like = LikeModel(
        movie_id=data.movie_id,
        user_id=user_id,
        rating=LikeModel.get_max_rating()
        if data.rating == response_models.RatingLike.LIKE
        else LikeModel.get_min_rating(),
    )
    try:
        item = await like_service.add(like)
    except ItemAlreadyExists:
        raise HTTPException(status_code=HTTPStatus.CONFLICT)
    return response_models.RatingGetModel.from_service_model(item)


@router.delete(
    "/{user_id}/ratings/{rating_id}",
    summary="Удалить оценку фильма",
    tags=["Likes"],
    dependencies=[Depends(jwt_user_verify)],
)
async def rating_delete(
    user_id: UUID = Path(..., title="User ID"),
    rating_id: str = Path(..., title="Rating ID"),
    like_service=Depends(get_like_service),
):
    try:
        await like_service.delete(user_id, rating_id)
    except ItemNotFound:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)


@router.get(
    "/{user_id}/bookmarks/",
    summary="Получить все закладки пользователя",
    response_model=List[response_models.BookmarkGetModel],
    tags=["Bookmarks"],
    dependencies=[Depends(jwt_user_verify)],
)
async def bookmark_list(
    user_id: UUID = Path(..., title="User ID"),
    bookmark_service=Depends(get_bookmark_service),
) -> List[response_models.BookmarkGetModel]:
    bookmarks = await bookmark_service.get_list(user_id)

    return [
        response_models.BookmarkGetModel.from_service_model(bookmark)
        for bookmark in bookmarks
    ]


@router.get(
    "/{user_id}/bookmarks/{bookmark_id}",
    summary="Получить оценку пользователя по ID",
    response_model=response_models.BookmarkGetModel,
    tags=["Bookmarks"],
    dependencies=[Depends(jwt_user_verify)],
)
async def bookmark_get_by_id(
    user_id: UUID = Path(..., title="User ID"),
    bookmark_id: str = Path(..., title="Bookmark ID"),
    bookmark_service=Depends(get_bookmark_service),
) -> response_models.BookmarkGetModel:
    try:
        bookmark = await bookmark_service.get_bookmark(user_id, bookmark_id)
    except ItemNotFound:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    return response_models.BookmarkGetModel.from_service_model(bookmark)


@router.post(
    "/{user_id}/bookmarks/",
    summary="Добавить закладку",
    response_model=response_models.BookmarkGetModel,
    tags=["Bookmarks"],
    dependencies=[Depends(jwt_user_verify)],
)
async def bookmark_add(
    data: response_models.BookmarkAddModel,
    user_id: UUID = Path(..., title="User ID"),
    bookmark_service=Depends(get_bookmark_service),
) -> response_models.BookmarkGetModel:
    try:
        bookmark = await bookmark_service.add_bookmark(data.movie_id, user_id)
    except ItemAlreadyExists:
        raise HTTPException(status_code=HTTPStatus.CONFLICT)
    return response_models.BookmarkGetModel.from_service_model(bookmark)


@router.delete(
    "/{user_id}/bookmarks/{bookmark_id}",
    summary="Удалить закладку по ID",
    tags=["Bookmarks"],
    dependencies=[Depends(jwt_user_verify)],
)
async def bookmark_delete_by_id(
    user_id: UUID = Path(..., title="User ID"),
    bookmark_id: str = Path(..., title="Bookmark ID"),
    bookmark_service=Depends(get_bookmark_service),
):
    try:
        await bookmark_service.delete_bookmark(user_id, bookmark_id)
    except ItemNotFound:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)


@router.get(
    "/{user_id}/reviews/",
    summary="Получить все рецензии пользователя",
    response_model=List[response_models.ReviewGetModel],
    tags=["Reviews"],
    dependencies=[Depends(jwt_user_verify)],
)
async def reviews_list(
    user_id: UUID = Path(..., title="User ID"),
    review_service=Depends(get_review_service),
) -> List[response_models.ReviewGetModel]:
    items = await review_service.get_list(user_id)
    return [response_models.ReviewGetModel.from_service_model(item) for item in items]


@router.get(
    "/{user_id}/reviews/{review_id}",
    summary="Получить рецензию пользователя по ID",
    response_model=response_models.ReviewGetModel,
    tags=["Reviews"],
    dependencies=[Depends(jwt_user_verify)],
)
async def review_get_by_id(
    user_id: UUID = Path(..., title="User ID"),
    review_id: str = Path(..., title="Review ID"),
    review_service=Depends(get_review_service),
) -> response_models.ReviewGetModel:
    try:
        item = await review_service.get(user_id, review_id)
    except ItemNotFound:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    return response_models.ReviewGetModel.from_service_model(item)


@router.post(
    "/{user_id}/reviews/",
    summary="Добавить рецензию",
    response_model=response_models.ReviewGetModel,
    tags=["Reviews"],
    dependencies=[Depends(jwt_user_verify)],
)
async def review_add(
    data: response_models.ReviewAddModel,
    user_id: UUID = Path(..., title="User ID"),
    review_service=Depends(get_review_service),
) -> response_models.ReviewGetModel:
    try:
        item = await review_service.add(
            data.movie_id, user_id, data.text, data.user_rating
        )
    except ItemAlreadyExists:
        raise HTTPException(status_code=HTTPStatus.CONFLICT)
    return response_models.ReviewGetModel.from_service_model(item)


@router.delete(
    "/{user_id}/reviews/{review_id}",
    summary="Удалить рецензию по ID",
    tags=["Reviews"],
    dependencies=[Depends(jwt_user_verify)],
)
async def review_delete_by_id(
    user_id: UUID = Path(..., title="User ID"),
    review_id: str = Path(..., title="Bookmark ID"),
    review_service=Depends(get_review_service),
):
    try:
        await review_service.delete(user_id, review_id)
    except ItemNotFound:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)


@router.get(
    "/{user_id}/reviews/{review_id}/ratings",
    summary="Получить все оценки рецензий пользователя",
    tags=["Review ratings"],
    dependencies=[Depends(jwt_user_verify)],
)
async def review_rating_list(
    user_id: UUID = Path(..., title="User ID"),
    review_id: str = Path(..., title="Review ID"),
    review_rating_service=Depends(get_review_rating_service),
) -> List[response_models.ReviewRatingGetModel]:
    items = await review_rating_service.get_list(user_id, review_id)
    return [
        response_models.ReviewRatingGetModel.from_service_model(item) for item in items
    ]


@router.get(
    "/{user_id}/reviews/{review_id}/ratings/{rating_id}",
    summary="Получить оценку рецензии пользователя по ID",
    tags=["Review ratings"],
    dependencies=[Depends(jwt_user_verify)],
)
async def review_rating_get_by_id(
    user_id: UUID = Path(..., title="User ID"),
    review_id: str = Path(..., title="Review ID"),
    rating_id: str = Path(..., title="Review rating ID"),
    review_rating_service=Depends(get_review_rating_service),
) -> response_models.ReviewRatingGetModel:
    try:
        item = await review_rating_service.get(user_id, rating_id)
    except ItemNotFound:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    return response_models.ReviewRatingGetModel.from_service_model(item)


@router.post(
    "/{user_id}/reviews/{review_id}/ratings",
    summary="Добавить оценку рецензии",
    tags=["Review ratings"],
    dependencies=[Depends(jwt_user_verify)],
)
async def review_rating_add(
    data: response_models.ReviewRatingAddModel,
    user_id: UUID = Path(..., title="User ID"),
    review_id: str = Path(..., title="Review ID"),
    review_rating_service=Depends(get_review_rating_service),
) -> response_models.ReviewRatingGetModel:
    model = ReviewRatingModel(
        review_id=review_id,
        user_id=user_id,
        user_rating=ReviewRatingModel.get_max_rating()
        if data.rating == response_models.RatingLike.LIKE
        else ReviewRatingModel.get_min_rating(),
    )
    try:
        item = await review_rating_service.add(model)
    except ItemAlreadyExists:
        raise HTTPException(status_code=HTTPStatus.CONFLICT)
    return response_models.ReviewRatingGetModel.from_service_model(item)


@router.delete(
    "/{user_id}/reviews/{review_id}/ratings/{rating_id}",
    summary="Удалить оценку рецензию по ID",
    tags=["Review ratings"],
    dependencies=[Depends(jwt_user_verify)],
)
async def review_rating_delete_by_id(
    user_id: UUID = Path(..., title="User ID"),
    review_id: str = Path(..., title="Review ID"),
    rating_id: str = Path(..., title="Review rating ID"),
    review_rating_service=Depends(get_review_rating_service),
):
    try:
        await review_rating_service.delete(user_id, rating_id)
    except ItemNotFound:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
