from fastapi import APIRouter

from app.routes.api import api_router
from app.routes.views import view_router
from app.routes.websockets import ws_router

router = APIRouter()
router.include_router(api_router)
router.include_router(view_router)
router.include_router(ws_router)
