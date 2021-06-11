from fastapi.routing import APIRouter

from app.core import settings

user_router = APIRouter()


router = APIRouter(prefix=settings.API_STR_V1)
router.include_router(user_router)

