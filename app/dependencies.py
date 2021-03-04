from fastapi import Depends
from sqlalchemy.orm.session import Session as SessionType  # For IDE autocomplete

from . import db


class _SessionContextManager:
    def __init__(self):
        self.db = db.Session()

    def __enter__(self):
        return self.db

    # Todo: __aexit__?
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.close()


async def _get_session() -> SessionType:
    with _SessionContextManager() as session:
        yield session


get_session = Depends(_get_session)
