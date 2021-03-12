from fastapi import APIRouter

# Avoid circular imports by importing models AFTER Base
# Importing app.models adds the models to the base
from app.database import Base
import app.models
from app.routes import router


def create_all(**kw):
    pass


def drop_all(**kw):
    pass


__all__ = ["create_all", "drop_all", "router"]
