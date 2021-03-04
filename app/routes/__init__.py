from fastapi import APIRouter

from .api import router as api_router
from .public import router as public_router
from .websocket import router as websocket_router

router = APIRouter()
router.include_router(api_router)
router.include_router(public_router)
router.include_router(websocket_router)

__all__ = ["router"]
