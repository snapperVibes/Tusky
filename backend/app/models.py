import enum

from sqlalchemy import DDL, event
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import (
    Column as C,
    ForeignKey as FK,
    CheckConstraint,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID, ExcludeConstraint, ENUM, JSONB
from sqlalchemy.sql import functions
from sqlalchemy.sql.sqltypes import (
    INT,
    TEXT,
    BOOLEAN as BOOL,
    VARCHAR,
    DateTime,
    LargeBinary,
)


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
# Todo: Sadly, it looks like I implemented my primary keys in a way that doesn't scale
#   (As this is a pet-project/resume-builder, it is fun to over-engineer Tusky)
#   I want to use a SnowFlake implementation, but I have some concerns with the protocol
#   Namely, a SnowFlake's epoch is only 69 years long, and Twitter has deprecated them
#   https://github.com/twitter-archive/snowflake/tree/snowflake-2010
#   It seems that public facing snowflakes are okay as primary keys
# Todo: ondelete should be a per-column option


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


def UserFK(**kw):
    return C(UUID(as_uuid=True), FK("user.id"), nullable=False, **kw)


def RoomFK(**kw):
    return C(UUID(as_uuid=True), FK("room.id"), nullable=False, **kw)


def QuizFK(**kw):
    return C(
        UUID(as_uuid=True),
        FK("quiz.id", ondelete="CASCADE"),
        nullable=False,
        **kw,
    )


#######################################################################################
class User(Base):
    # Todo: as it stands, one can get someone else's number
    #  if the person with the highest number deletes their account
    __table_args__ = (UniqueConstraint("identifier_name", "number"),)
    id = ID()
    ts = TS()
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
    number = C(INT)  # Number starts as null, but is immediately set to the next number
    hashed_password = C(TEXT, nullable=False)
    is_superuser = C(BOOL, default=False, nullable=False)
    is_active = C(BOOL, default=True)
    quizzes = relationship("Quiz", back_populates="owner")

    @property
    def name_and_number(self):
        # User(name="foo", number=255) -> "foo#0255"
        return self.display_name + "#" + str(self.number).zfill(4)


class Room(Base):
    # Guarantees unique room code (of currently active rooms).
    # Two rooms can not share the same code if they are both active.
    # Todo: add time component so people can't get the same room right after each other
    __table_args__ = (
        ExcludeConstraint(("code", "="), where=(text("is_active = TRUE"))),
    )
    id = ID()
    ts = TS()
    code = C(TEXT, nullable=False)
    is_active = C(BOOL)
    owner_id = UserFK()
    session = relationship("QuizSession")


class Quiz(Base):
    __table_args__ = (UniqueConstraint("title", "owner_id"),)
    id = ID()
    ts = TS()
    owner_id = UserFK()
    owner = relationship("User", back_populates="quizzes")
    is_public = C(BOOL, default=True)
    content = C(JSONB)





########################################################################################
_to_identifier_func = DDL(
    """\
CREATE FUNCTION _to_identifier_func() RETURNS TRIGGER AS $$
    import unicodedata
    disp_name = TD["new"]["display_name"]
    id_name = unicodedata.normalize("NFKD", disp_name).lower()
    TD["new"]["identifier_name"] = id_name
    if id_name.__contains__("admin"):
        count_row = plpy.execute("SELECT count(display_name) FROM public.user WHERE display_name='admin';")
        if count_row[0]['count'] > 0:
            raise ValueError("Name cannot be admin.")
        TD["new"]["number"] = 0
    if id_name.__contains__("#"):
        raise ValueError("The normalized name cannot contain the hash symbol")
    if len(id_name) > 32:
        raise ValueError("The normalized name cannot be longer than 32 characters")
    return "MODIFY"
$$ LANGUAGE PLPYTHON3U;"""
)
_to_identifier_trigger = DDL(
    """\
CREATE TRIGGER _to_identifier_trigger BEFORE INSERT OR UPDATE on public.user
FOR EACH ROW EXECUTE PROCEDURE _to_identifier_func();"""
)


def set_event_listeners():
    event.listen(
        User.__table__,
        "after_create",
        _to_identifier_func.execute_if(dialect="postgresql"),
    )

    event.listen(
        User.__table__,
        "after_create",
        _to_identifier_trigger.execute_if(dialect="postgresql"),
    )
