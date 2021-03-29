from fastapi import APIRouter

from app.core import settings
from app.routes.api import api_router
from app.routes.websockets import ws_router

router = APIRouter()
router.include_router(api_router, prefix=settings.API_V1_STR)
router.include_router(ws_router)
