from fastapi import Depends
from sqlalchemy.orm.session import (
    sessionmaker,
    Session as SessionType,
)  # For IDE autocomplete

from . import db

Session = sessionmaker(autocommit=False, autoflush=True, bind=db.engine, future=True)


class _SessionContextManager:
    def __init__(self):
        self.db = Session()

    def __enter__(self):
        return self.db

    # Todo: __aexit__?
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.close()


async def _get_db() -> SessionType:
    with _SessionContextManager() as session:
        yield session


get_session = Depends(_get_db)
