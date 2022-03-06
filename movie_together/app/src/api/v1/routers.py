from fastapi import APIRouter

from movie_together.app.src.api.v1.room import room_router

api_v1_router = APIRouter()

api_v1_router.include_router(room_router, prefix='/room', tags=['room'])
