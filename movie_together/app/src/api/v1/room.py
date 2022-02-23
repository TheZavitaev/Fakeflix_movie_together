from fastapi import APIRouter, Depends
from starlette.requests import Request

from movie_together.app.src.core.auth.decorators import login_required
from movie_together.app.src.models.models import ResponseModel
from movie_together.app.src.services.room import RoomService, get_room_service

room_router = APIRouter()


@room_router.post('/', response_model=ResponseModel)
@login_required()
async def create_room(
        request: Request,
        service: RoomService = Depends(get_room_service),
) -> ResponseModel:
    error = await service.create_user_room(user_id=request.user.pk)
    if error:
        return ResponseModel(success=False, errors=[error])
    return ResponseModel(success=True)
