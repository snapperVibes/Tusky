from typing import Generator

from app.database import SessionLocal


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_active_user():
    pass


def get_current_active_superuser():
    pass
