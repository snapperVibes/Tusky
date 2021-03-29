__all__ = [
    # Functions
    "create_all",
    "drop_all",
]

from sqlalchemy.exc import InternalError

from app.core import settings, security
from app import crud, schemas, main
from app.models import Base
from app.database import engine, SessionLocal


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

