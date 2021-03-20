from fastapi import APIRouter

from app import settings
from app.routes.api.login import router as login_router
from app.routes.api.rooms import router as rooms_router
from app.routes.api.users import router as users_router

api_router = APIRouter()
api_router.include_router(login_router, prefix=settings.API_V1_STR, tags=["login"])
api_router.include_router(
    users_router, prefix=settings.API_V1_STR + "/users", tags=["users"]
)
api_router.include_router(
    rooms_router, prefix=settings.API_V1_STR + "/rooms", tags=["rooms"]
)
