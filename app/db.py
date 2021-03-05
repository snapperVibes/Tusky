import os

from sqlalchemy import text
from sqlalchemy.future import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session as SessionType


def get_uri() -> str:
    # https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNSTRING
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    dbname = os.getenv("POSTGRES_DB")
    port = os.getenv("POSTGRES_PORT")
    host = os.getenv("POSTGRES_HOST")
    return f"postgresql://{user}:{password}@{host}:{port}/{dbname}"


uri = get_uri()
engine = create_engine(uri, echo=True)  # Show SQL Statements for development
Base = declarative_base()
Session = sessionmaker(autocommit=False, autoflush=True, bind=engine, future=True)



