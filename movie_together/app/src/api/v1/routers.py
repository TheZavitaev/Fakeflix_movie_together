from api.v1.room import room_router
from fastapi import APIRouter

api_v1_router = APIRouter()

api_v1_router.include_router(room_router, prefix='/room', tags=['room'])
