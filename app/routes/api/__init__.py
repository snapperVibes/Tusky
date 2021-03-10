from fastapi import APIRouter

from app.routes.api.room import router as room_router
from app.routes.api.user import router as user_router


api_router = APIRouter()
api_router.include_router(user_router, prefix="/users", tags=["users"])
api_router.include_router(room_router, prefix="/rooms", tags=["rooms"])
