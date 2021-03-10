from fastapi import APIRouter

# Avoid circular imports by importing models AFTER Base
# Importing app.models adds the models to the base
from app.database import Base
import app.models
from app.routes.api import api_router
from app.routes.views import view_router
from app.routes.websocket import ws_router

router = APIRouter()
router.include_router(api_router)
router.include_router(view_router)
router.include_router(ws_router)


def create_all(**kw):
    pass


def drop_all(**kw):
    pass


__all__ = ["create_all", "drop_all", "router"]
