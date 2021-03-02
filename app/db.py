import os

from sqlalchemy import MetaData
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

# metadata = MetaData(
#     naming_convention={
#         "ix": "ix__%(column_0_label)s",
#         "uq": "uq__%(table_name)s__%(column_0_name)s",
#         "ck": "ck__%(table_name)s__%(column_0_name)s",
#         "fk": "fk__%(table_name)s__%(column_0_name)s__%(reffered_table_name)s",
#         "pk": "pk__%(table_name)s",
#     }
# )

# Base = declarative_base(metadata=metadata)

Base = declarative_base()
