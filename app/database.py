from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import sessionmaker

from app.core import settings


@as_declarative()
class Base:
    __name__: str

    # @declared_attr
    # def __tablename__(cls) -> str:
    # """ Generate __tablename__ automatically """
    #     n = cls.__name_s_
    #     # ExampleTable -> example_table
    #     return n[0].lower() + "".join("_" + x.lower() if x.isupper() else x for x in n[1:])


engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
