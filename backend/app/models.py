import enum

from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.schema import (
    Column as C,
    ForeignKey as FK,
    CheckConstraint,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID, ExcludeConstraint, ENUM
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
# Todo: Sadly, it looks like I implemented my primary keys wrong
#  I want to use a SnowFlake implementation, but I have some concerns with the protocol
#  Namely, a SnowFlake's epoch is only 69 years long, and Twitter has deprecated them
#  https://github.com/twitter-archive/snowflake/tree/snowflake-2010
#  It seems that public facing snowflakes are okay as primary keys
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


def QuizFK(**kw):
    return C(UUID(as_uuid=True), FK("quiz.id"), nullable=False, **kw)


def QuestionFK(**kw):
    return C(UUID(as_uuid=True), FK("question.id"), nullable=False, **kw)


def AnswerFK(**kw):
    # Todo: This one is unique becuase nullable=True;
    #  since it breaks the pattern, should it be removed?
    return C(UUID(as_uuid=True), FK("answer.id"), nullable=True, **kw)


def ImageFK(**kw):
    return C(UUID(as_uuid=True), FK("image.id"), nullable=False, **kw)


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
    number = C(INT, nullable=False)
    hashed_password = C(TEXT, nullable=False)
    is_superuser = C(BOOL, default=False, nullable=False)
    is_active = C(BOOL, default=True)
    # profile_picture = ImageFK()

    @property
    def name_and_number(self):
        # User(name="foo", number=255) -> "foo#0255"
        return self.display_name + "#" + str(self.number).zfill(4)


class Room:
    # Guarantees unique room code (of currently active rooms).
    # Two rooms can not share the same code if they are both active.
    # Todo: add time component so people can't get the same room right after each other
    __table_args__ = (ExcludeConstraint(("code", "="), where=(text("active = TRUE"))),)
    id = ID()
    ts = TS()
    code = C(TEXT, nullable=False)
    active = C(BOOL)


class Quiz(Base):
    __table_args__ = (UniqueConstraint("name", "owner"),)
    id = ID()
    ts = TS()
    name = C(
        VARCHAR(32),
        CheckConstraint(min_size("name", 1)),
        nullable=False,
    )
    owner = UserFK()
    is_public = C(BOOL, default=True)


class Question(Base):
    id = ID()
    ts = TS()
    quiz_fk = QuizFK()
    query = C(TEXT)


class AnswerIdentifier(enum.Enum):
    # It doesn't feel worth the effort to allow custom answer identifiers
    LETTER = "letter"
    NUMERIC = "numeric"


class Answer(Base):
    """
    Types of Answers:
        Radio: Only one answer of type Radio can be correct per question
        Selection: 0 or more answers of type selection can be selected
        Order: Draggable answer whose correctness is decided by its position
        ShortAnswer: Student's write in answers compared to a selection of correct answers
        Essay: Teacher manually grades written responses"""

    # Todo: ExcludeConstraint where only one null previous_answer per question
    id = ID()
    ts = TS()
    question_id = QuestionFK()
    previous_answer = AnswerFK()
    text = C(TEXT)
    # image = ImageFK()


class Image(Base):
    id = ID()
    ts = TS()
    uploaded_by = UserFK()
    filename = C(TEXT, nullable=False)
    public_code = C(TEXT, nullable=False)  # Todo: Discuss optimal public facing name
    data = C(LargeBinary, nullable=False)
    description = C(TEXT)
    image = ImageFK()
