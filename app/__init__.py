from .db import Base, engine
from .routes import router


def create_all(**kw):
    """ Create all tables """
    return Base.metadata.create_all(engine, **kw)


def drop_all(**kw):
    """ Drop all tables """
    return Base.metadata.drop_all(engine, **kw)


__all__ = ["create_all", "drop_all", "router"]
