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
    __table_args__ = (UniqueConstraint("name", "number"),)
    id = ID()
    ts = TS()
    name = C(
        VARCHAR(32),
        CheckConstraint(min_size("name", 1)),
        nullable=False,
    )
    # Todo: Number validation
    number = C(INT, nullable=False)
    hashed_password = C(TEXT, nullable=False)
    is_superuser = C(BOOL, default=False, nullable=False)
    is_active = C(BOOL, default=True)
