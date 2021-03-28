__all__ = [
    # Functions
    "create_all",
    "drop_all",
    "init_app",
    # # core
    # # "settings"
    # # "security",
    # # misc
    # # # "router"
    # # modules
    # "crud",
    # "database",
    # "exceptions",
    # "models",
    # "schemas",
]

from os import path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from sqlalchemy.exc import InternalError

from app import crud, schemas
from app.core import settings, security
from app.models import Base
from app.database import engine as engine, SessionLocal as SessionLocal
from app.routes import router

_HERE = path.dirname(path.realpath(__file__))


def create_all(**kw) -> bool:
    # Create the tables
    Base.metadata.create_all(engine, **kw)
    db = SessionLocal()
    # Add the super user
    super_user = schemas.UserCreate(
        display_name=settings.FIRST_SUPERUSER,
        password=settings.FIRST_SUPERUSER_PASSWORD,
        is_superuser=True,
    )
    try:
        crud.user.create(db, obj_init=super_user)
    except InternalError:
        return False
    return True


def drop_all(**kw):
    Base.metadata.drop_all(engine, **kw)


def init_app():
    app = FastAPI()
    app.include_router(router)
    app.mount(
        "/static", StaticFiles(directory=path.join(_HERE, "static")), name="static"
    )
    return app
