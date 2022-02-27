from http import HTTPStatus
from uuid import UUID

from core.exceptions import InsertEventTimeout
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from models.models import ViewedFrame as ServiceViewedFrame
from pydantic import BaseModel
from service.movie_progress import (
    AbstractMovieProgressService,
    get_movie_progress_service,
)

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class ViewedFrame(BaseModel):
    movie_id: UUID
    movie_timestamp: int


@router.post(
    '/',
    summary="Прогресс просмотра фильма",
    description="Записать прогресс просмотра фильма",
)
async def movie_progress_add(
        event: ViewedFrame,
        movie_progress_service: AbstractMovieProgressService = Depends(get_movie_progress_service),
        token: str = Depends(oauth2_scheme),
):
    # don't verify JWT secret. Only get user id
    payload = jwt.decode(token, 'dummy', options={"verify_signature": False})
    try:
        user_id = payload['user_id']
    except KeyError:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail='Invalid token')
    frame = ServiceViewedFrame(
        user_id=user_id,
        movie_id=event.movie_id,
        movie_timestamp=event.movie_timestamp,
    )

    try:
        await movie_progress_service.add(frame)
    except InsertEventTimeout as error:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=error)
