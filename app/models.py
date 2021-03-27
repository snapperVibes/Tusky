import inspect
from typing import NamedTuple, Callable

# import plpy_man  # PlPython Manager
# from plpy_man.mocks import GD, TD
from sqlalchemy import DDL, event, func
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.schema import (
    Column as C,
    CheckConstraint,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import functions
from sqlalchemy.sql.sqltypes import INT, TEXT, BOOLEAN as BOOL, VARCHAR, DateTime


@as_declarative()
class Base:
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        """ Generate __tablename__ automatically """
        n = cls.__name__
        # ExampleTable -> example_table
        return n[0].lower() + "".join(
            "_" + x.lower() if x.isupper() else x for x in n[1:]
        )


# CheckConstraint validates at the database level
# Validate validates at the Model level
# In general, use the pydantic.validator decorator to do python-level validation
########################################################################################
# Constraints
def min_size(column: str, minimum) -> str:
    return text(f"{functions.char_length(column)} >= :min").bindparams(min=minimum)


def does_not_contain(column: str, regex: str):
    return text(f"NOT f{column} like {str}")


#######################################################################################
# Functions for common columns
def ID(**kw):
    # return C(INT, IDENTITY(), primary_key=True, **kw)
    return C(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
        **kw,
    )


def TS(**kw):
    return C(DateTime, server_default=functions.now(), **kw)


#######################################################################################
class User(Base):
    # Todo: as it stands, one can get someone else's number
    #  if the person with the highest number deletes their account
    __table_args__ = (UniqueConstraint("identifier_name", "number"),)
    id = ID()
    ts = TS()
    # We're lucky Postgres13 is out,
    #  otherwise we'd have to write our own PLPython3U solution :P
    display_name = C(
        VARCHAR(32),
        CheckConstraint(min_size("display_name", 1)),
        nullable=False,
    )
    identifier_name = C(
        VARCHAR(32),
        CheckConstraint(min_size("identifier_name", 1)),
        nullable=False,
    )
    # Todo: Number validation
    number = C(INT, nullable=False)
    hashed_password = C(TEXT, nullable=False)
    is_superuser = C(BOOL, default=False, nullable=False)
    is_active = C(BOOL, default=True)

    @property
    def name_and_number(self):
        # User(name="foo", number=255) -> "foo#0255"
        return self.display_name + "#" + str(self.number).zfill(4)
