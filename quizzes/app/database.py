from sqlalchemy.future import create_engine
from sqlalchemy.orm import sessionmaker, Session

# Import all SQL Alchemy models before initializing database to ensure SQL Alchemy sets things up properly
from sqlalchemy.pool import SingletonThreadPool

from app.models import Base
from app.core import settings

engine = create_engine(settings.SQLALCHEMY_URI, echo=True)
SessionLocal = sessionmaker(engine, autoflush=False, autocommit=False)


def init_db(db: Session) -> None:
    # We don't use Alembic yet
    Base.metadata.create_all(bind=engine)


def drop_db(db: Session) -> None:
    # We don't use Alembic yet
    Base.metadata.drop_all(bind=engine)
