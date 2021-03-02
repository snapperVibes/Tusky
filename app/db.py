import enum
import os

from sqlalchemy import (
    LargeBinary as BLOB,
    BOOLEAN as BOOL,
    CheckConstraint,
    Column as C,
    DateTime as DATETIME,
    Enum as ENUM,
    ForeignKey as FK,
    Identity as IDENTITY,
    INT,
    NUMERIC,
    TEXT,
    VARCHAR,
    PrimaryKeyConstraint,
    UniqueConstraint,
)
from sqlalchemy.future import create_engine
from sqlalchemy.sql import functions
from sqlalchemy.orm import declarative_base, declared_attr, sessionmaker, validates

from .types import Role


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
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# CheckConstraint validates at the database level
# Validate validates at the Model level
# fmt: off  | It's on you to maintain formatting (Todo: snapfmt)
########################################################################################
# Constraints
# Todo: I'm fairly certain functions.char_length can be used somehow
#  instead of this wrapper. Figure it out
#  This whole function smells.
def MIN_SIZE(column: str, minimum) -> str:
    # CHAR_LENGTH is a built-in postgres string function
    # https://www.postgresql.org/docs/13/functions-string.html#FUNCTIONS-STRING-OTHER
    return f"CHAR_LENGTH({column}) >= {minimum}"


########################################################################################
# Factory functions for common columns to ease typing and reading of repeated text
def ID(**kw):         return C(INT, IDENTITY(), primary_key=True, **kw)
def TS(**kw):         return C(DATETIME, server_default=functions.now(), **kw)
def UserFK(**kw):     return C(INT, FK("users.id"), nullable=False, **kw)
def QseFK(**kw):      return C(INT, FK("quiz_session_events.id"), nullable=False, **kw)
def QuizFK(**kw):     return C(INT, FK("quizzes.id"), nullable=False, **kw)
def QuestionFK(**kw): return C(INT, FK("questions.id"), nullable=False, **kw)
def AnswerFK(**kw):   return C(INT, FK("answers.id"), nullable=False, **kw)
def ImageFK(**kw):    return C(INT, FK("images.id"), nullable=False, **kw)


########################################################################################
# Models
# The database is normalized to a reasonable level.
# Todo: Choose naming schema
class SiteRole(enum.Enum):
    SUPER_ADMIN = Role("Super Admin", "🦸")
    ADMIN       = Role("Admin", "👑")
    PLEBEIAN    = Role("User", "🙂")


class User(Base):
    __tablename__ = "users"
    # User names must be between 1 and 32 characters long
    id        = ID()
    ts        = TS()
    name      = C(VARCHAR(32), CheckConstraint(MIN_SIZE("name", 1)), nullable=False)
    salt      = C(TEXT, nullable=False)
    password  = C(TEXT, nullable=False)
    site_role = C(ENUM(SiteRole), nullable=False)

    UniqueConstraint("name", "number")

    @validates("name")
    def validate_name(self, _, name) -> str:
        if 1 <= len("name"):
            return name
        raise ValueError("User name must be between 1 and 32 characters.")


class EmailAddress(Base):
    __tablename__ = "email_addresses"
    # Application Techniques for Checking and Transformation of Names:
    #   https://tools.ietf.org/html/rfc3696
    id         = ID()
    ts         = TS()
    # Todo: Email validation
    local      = C(VARCHAR(64), CheckConstraint(MIN_SIZE("local", 1)), nullable=False)
    domain     = C(VARCHAR(255), CheckConstraint(MIN_SIZE("domain", 1)), nullable=False)
    verified   = C(BOOL)
    verifiedts = C(DATETIME)

    UniqueConstraint("local", "domain")


class LinkUserToEmailAddresses(Base):
    __tablename__ = "link_user_to_email_addresses"
    user          = UserFK(primary_key=True)
    email_address = C(INT, FK("email_addresses.id"), primary_key=True)
    # visibility    = C()  # Todo: Email visibility


class Image(Base):
    __tablename__ = "images"
    id          = ID()
    ts          = TS()
    uploaded_by = UserFK()
    filename    = C(TEXT, nullable=False)
    public_code = C(TEXT, nullable=False)  # Todo: Discuss optimal public facing name
    data        = C(BLOB, nullable=False)
    description = C(TEXT)


#######################################################################################
class Room(Base):
    __tablename__ = "rooms"
    # Todo: Consider using Redis for storing ephemeral details of rooms
    id = ID()
    ts = TS()
    # Todo: Verify code unique among currently valid rooms
    #  Make a function like
    #    CREATE FUNCTION room_code_validator(_code TEXT)
    #    RETURNS BOOL AS
    #    BEGIN
    #    IF COUNT(SELECT FROM room WHERE valid=true AND code=_code) > 0:
    #        return True
    #    return False
    #  and use it to validate that code is unique
    code = C(TEXT)
    valid = C(BOOL)


class RoomRole(enum.Enum):
    TEACHER = Role("Teacher", "🧑‍🏫")  # Zero-width join
    STUDENT = Role("Student", "🧑‍🎓")  # Zero-width join


class RoomEvent(Base):
    """
    Room Events:
        Teacher:Room:{}
        Teacher:QuizSession:{Start, Finish}
        Student:QuizSession:{Join, Leave}
        Either:Room:{Join, Leave, Invite, message

    """
    # Temp comment to help keep work in one place:
    #   UserRole: SuperAdmin, Admin, Plebeian PLEBEIAN
    #   EntityType: Room, QuizSession, Quiz, Question, Answer
    #   Action: Started, Finished, Join, Leave, Added, Modified (Requires old and new), Selected, locked-in Removed,
    __tablename__ = "room_events"
    id      = ID()
    ts      = TS()
    room_id = C(INT, FK("rooms.id"), nullable=False)


#######################################################################################
class Quiz(Base):
    __tablename__ = "quizzes"
    id = ID()
    ts = TS()


class Question(Base):
    __tablename__ = "questions"
    id      = ID()
    ts      = TS()
    quiz_id = QuizFK()
    image   = ImageFK()


class Answer(Base):
    """
    Types of Answers:
        Radio: Only one answer of type Radio can be correct per question
        Selection: 0 or more answers of type selection can be selected
        Order: Draggable answer whose correctness is decided by its position
        ShortAnswer: Student's write in answers compared to a selection of correct answers
        Essay: Teacher manually grades written responses """
    __tablename__ = "answers"
    id          = ID()
    ts          = TS()
    question_id = QuestionFK()
    identifier  = C(TEXT)
    # Todo: Add validation that ensures two answers on the same question can't have the same order
    # Todo: Ensure order starts at 1 and every gap is filled
    order       = C(INT, nullable=False)
    image       = ImageFK()


class RadioAnswer(Base):
    __tablename__ = "answers_type_radio"
    answer_id = AnswerFK(primary_key=True)
    correct  = C(BOOL, nullable=False)
    value    = C(NUMERIC, default=1)   # Todo: default = lambda (self): 1 if correct else 0
    PrimaryKeyConstraint("answer_id")


class SelectionAnswer(Base):
    __tablename__ = "answers_type_selection"
    answer_id = AnswerFK(primary_key=True)
    correct   = C(BOOL, nullable=False)
    value     = C(NUMERIC, default=1)
    PrimaryKeyConstraint("answer_id")


class OrderAnswer(Base):
    __tablename__ = "answers_type_order"
    answer_id        = AnswerFK(primary_key=True)
    correct_position = C(INT, nullable=False)
    value            = C(NUMERIC, default=1)   # Todo: default = lambda (self): 1 if correct else 0
    PrimaryKeyConstraint("answer_id")


class ShortAnswer(Base):
    __tablename__ = "answers_type_short"
    answer_id = AnswerFK(primary_key=True)
    PrimaryKeyConstraint("answer_id")


class CorrectShortAnswers(Base):
    __tablename__ = "answers_type_short_answer"
    answer_id = AnswerFK(primary_key=True)
    correct   = C(TEXT, nullable=False)
    value     = C(NUMERIC, default=1)
    PrimaryKeyConstraint("answer_id", "correct")


class EssayAnswer(Base):
    __tablename__ = "answers_type_essay"
    answer_id = AnswerFK(primary_key=True)
    PrimaryKeyConstraint("answer_id")


class QuizSession(Base):
    __tablename__ = "quiz_sessions"
    id      = ID()
    ts      = TS()
    quiz_id = QuizFK()
    room_id = C(INT, FK("rooms.id"))


class QuizSessionEvent(Base):
    """
    # todo: use actual expression language
    There are many types of event types, but they all follow the same schema:
        UserRole:EntityType:Action

    Event Types:
        Admin:Quiz:{{start | finish}}
        Admin:Question:{{start | finish | modify | remove}}
        Admin:Answer:{{add | modify | remove}}
        Plebeian:Quiz:{{start | finish}}
        Plebeian:Question:{{start | finish}}
        Plebeian:Answer:{{select | lock-in}}
    """
    __tablename__ = "quiz_session_events"
    # Order taxonomy for copy-editors (Coders shouldn't have to worry about it.)
    #   UserRole: SuperAdmin, Admin, Plebeian
    #   EntityType: Quiz, Question, Answer
    #   Action: Started, Finished, Added, Modified (Requires old and new), Selected, locked-in Removed,
    # We purposefully do not give Admins the ability to add questions mid quiz
    # Adding questions mid quiz seems like a good way for things to fall apart
    id              = ID()
    ts              = TS()
    quiz_session_id = C(INT, FK("quiz_sessions.id"), nullable=False)
    user_id         = UserFK()


class _qse:
    """ Quiz Session Event __tablename__ mixin to reduce typing during development """
    @declared_attr
    def __tablename__(cls):
        _QSE, entity_type, action = cls.__name__.split("_")
        # Split action on capital letters
        action = "".join("_" + x.lower() if x.isupper() else x for x in action)
        return f"quiz_session_events__{entity_type.lower()}__{action}"


class QSE_Teacher_QuizStarted(Base, _qse):
    quiz_session_event_id = QseFK(primary_key=True)


class QSE_Teacher_QuizFinished(Base, _qse):
    quiz_session_event_id = QseFK(primary_key=True)


class QSE_Teacher_QuestionStarted(Base, _qse):
    quiz_session_event_id = QseFK(primary_key=True)
    # Todo: Validation that you can't start the same question twice before finishing it
    question_id           = QuestionFK(primary_key=True)


class QSE_Teacher_QuestionFinished(Base, _qse):
    quiz_session_event_id = QseFK(primary_key=True)
    question_id           = QuestionFK(primary_key=True)


class QSE_Teacher_QuestionModified(Base, _qse):
    quiz_session_event_id = QseFK(primary_key=True)
    old_question          = QuestionFK(primary_key=True)
    new_question          = QuestionFK()


class QSE_Teacher_QuestionRemoved(Base, _qse):
    quiz_session_event_id = QseFK(primary_key=True)
    question_id           = QuestionFK(primary_key=True)


class QSE_Teacher_AnswerAdded(Base, _qse):
    quiz_session_event_id = QseFK(primary_key=True)
    new_answer            = AnswerFK(primary_key=True)


class QSE_Teacher_AnswerModified(Base, _qse):
    quiz_session_event_id = QseFK(primary_key=True)
    old_answer            = AnswerFK(primary_key=True)
    new_answer            = AnswerFK()


class QSE_Teacher_AnswerRemoved(Base, _qse):
    quiz_session_event_id = QseFK(primary_key=True)
    answer_id             = AnswerFK(primary_key=True)


class QSE_Student_QuizStarted(Base, _qse):
    quiz_session_event_id = QseFK(primary_key=True)


class QSE_Student_QuizFinished(Base, _qse):
    quiz_session_event_id = QseFK(primary_key=True)


class QSE_Student_QuestionStarted(Base, _qse):
    quiz_session_event_id = QseFK(primary_key=True)
    question_id           = QuestionFK(primary_key=True)


class QSE_Student_QuestionFinished(Base, _qse):
    quiz_session_event_id = QseFK(primary_key=True)
    question_id           = QuestionFK(primary_key=True)


class QSE_Student_AnswerSelected(Base, _qse):
    quiz_session_event_id = QseFK(primary_key=True)
    # Todo: Implement human waiting period:
    #  Perhaps don't add event if more than 3 selections happen in less than .2 seconds?
    answer_id             = AnswerFK(primary_key=True)


class QSE_Student_AnswerLockedIn(Base, _qse):
    quiz_session_event_id = QseFK(primary_key=True)
    answer_id             = AnswerFK(primary_key=True)


# fmt: on
