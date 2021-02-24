import os

from sqlalchemy.future import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


def get_uri() -> str:
    # https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNSTRING
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    dbname = os.getenv("POSTGRES_DB")
    port = os.getenv("POSTGRES_PORT")
    host = os.getenv("POSTGRES_HOST")
    return f"postgresql://{user}:{password}@{host}:{port}/{dbname}"


uri = get_uri()
engine = create_engine(uri)
SessionalLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
