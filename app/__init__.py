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
from sqlalchemy.exc import IntegrityError

from app import crud, schemas
from app.core import settings, security
from app.models import Base
from app.database import engine as engine, SessionLocal as SessionLocal
from app.routes import router

_HERE = path.dirname(path.realpath(__file__))


def create_all(**kw) -> bool:
    # Create the tables
    Base.metadata.create_all(engine, **kw)
    # Add the super user
    super_user = schemas.UserCreate(
        name=settings.FIRST_SUPERUSER,
        password=settings.FIRST_SUPERUSER_PASSWORD,
        number=0,
        is_superuser=True,
    )
    try:
        crud.user.create(SessionLocal(), obj_init=super_user)
    except IntegrityError:
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
