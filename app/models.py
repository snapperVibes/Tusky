import enum
import hashlib
import os
import random

from sqlalchemy.sql import functions
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.schema import (
    Column as C,
    CheckConstraint,
    ForeignKey as FK,
    PrimaryKeyConstraint,
    UniqueConstraint,
)
from sqlalchemy.orm import declared_attr, validates, Session
from sqlalchemy.sql.sqltypes import (
    LargeBinary as BLOB,
    BOOLEAN as BOOL,
    DateTime as DATETIME,
    Enum as ENUM,
    INT,
    NUMERIC,
    TEXT,
    VARCHAR,
)
from sqlalchemy.dialects.postgresql import BYTEA, UUID, ExcludeConstraint

from .db import Base
from .schema import Role


# CheckConstraint validates at the database level
# Validate validates at the Model level
########################################################################################
# Constraints
def min_size(column: str, minimum) -> str:
    return text(f"{functions.char_length(column)} >= :min").bindparams(min=minimum)


########################################################################################
# Factory functions for common columns
def ID(**kw):
    # return C(INT, IDENTITY(), primary_key=True, **kw)
    return C(
        UUID(),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
        **kw,
    )


def TS(**kw):
    return C(DATETIME, server_default=functions.now(), **kw)


def UserFK(**kw):
    return C(UUID, FK("users.id"), nullable=False, **kw)


def QseFK(**kw):
    return C(UUID, FK("quiz_session_events.id"), nullable=False, **kw)


def QuizFK(**kw):
    return C(UUID, FK("quizzes.id"), nullable=False, **kw)


def QuestionFK(**kw):
    return C(UUID, FK("questions.id"), nullable=False, **kw)


def AnswerFK(**kw):
    return C(UUID, FK("answers.id"), nullable=False, **kw)


def ImageFK(**kw):
    return C(UUID, FK("images.id"), nullable=False, **kw)


def EmailAddressFK(**kw):
    return C(UUID, FK("email_addresses.id"), **kw)


def RoomFK(**kw):
    return C(UUID, FK("rooms.id"), nullable=False, **kw)


def QuizSessionFK(**kw):
    return C(UUID, FK("quiz_sessions.id"), nullable=False)


########################################################################################
# Models
# The database is normalized to a reasonable level.
# Todo: Choose naming schema
class SiteRole(enum.Enum):
    SUPER_ADMIN = Role("Super Admin", "🦸")
    ADMIN = Role("Admin", "👑")
    PLEBEIAN = Role("User", "🙂")


class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint("name", "number"),
    )
    # User names must be between 1 and 32 characters long
    id = ID()
    ts = TS()
    name = C(VARCHAR(32), CheckConstraint(min_size("name", 1)), nullable=False)
    number = C(
        INT,
        nullable=False
    )
    key = C(BYTEA, nullable=False)
    site_role = C(ENUM(SiteRole), default=SiteRole.PLEBEIAN, nullable=False)


    @validates("name")
    def validate_name(self, _, name) -> str:
        if 1 <= len("name"):
            return name
        raise ValueError("User name must be between 1 and 32 characters.")


class EmailAddress(Base):
    __tablename__ = "email_addresses"
    __table_args__ = (
        UniqueConstraint("mailbox", "hostname"),
)
    # Application Techniques for Checking and Transformation of Names:
    #   https://tools.ietf.org/html/rfc3696
    id = ID()
    ts = TS()
    # Todo: Email validation
    mailbox = C(VARCHAR(64), CheckConstraint(min_size("local", 1)), nullable=False)
    hostname = C(VARCHAR(255), CheckConstraint(min_size("domain", 1)), nullable=False)
    verified = C(BOOL)
    verifiedts = C(DATETIME)



class LinkUserToEmailAddresses(Base):
    __tablename__ = "link_user_to_email_addresses"
    user = UserFK(primary_key=True)
    email_address = EmailAddressFK(primary_key=True)
    # visibility    = C()  # Todo: Email visibility


class Image(Base):
    __tablename__ = "images"
    id = ID()
    ts = TS()
    uploaded_by = UserFK()
    filename = C(TEXT, nullable=False)
    public_code = C(TEXT, nullable=False)  # Todo: Discuss optimal public facing name
    data = C(BLOB, nullable=False)
    description = C(TEXT)


class Room(Base):
    __tablename__ = "rooms"
    # Guarantees unique room code (of currently active rooms).
    # Two rooms can not share the same code if they are both active.
    # Todo: add time component so people can't get the same room right after each other
    __table_args__ = (ExcludeConstraint(("code", "="), where=(text("active = TRUE"))),)
    id = ID()
    ts = TS()
    code = C(TEXT, nullable=False)
    active = C(BOOL)


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
    id = ID()
    ts = TS()
    room_id = RoomFK()


class Quiz(Base):
    __tablename__ = "quizzes"
    id = ID()
    ts = TS()


class Question(Base):
    __tablename__ = "questions"
    id = ID()
    ts = TS()
    quiz_id = QuizFK()
    image = ImageFK()


class Answer(Base):
    """
    Types of Answers:
        Radio: Only one answer of type Radio can be correct per question
        Selection: 0 or more answers of type selection can be selected
        Order: Draggable answer whose correctness is decided by its position
        ShortAnswer: Student's write in answers compared to a selection of correct answers
        Essay: Teacher manually grades written responses"""

    __tablename__ = "answers"
    id = ID()
    ts = TS()
    question_id = QuestionFK()
    identifier = C(TEXT)
    # Todo: Add validation that ensures two answers on the same question can't have the same order
    # Todo: Ensure order starts at 1 and every gap is filled
    order = C(INT, nullable=False)
    image = ImageFK()


class RadioAnswer(Base):
    __tablename__ = "answers_type_radio"
    answer_id = AnswerFK(primary_key=True)
    correct = C(BOOL, nullable=False)
    value = C(NUMERIC, default=1)  # Todo: default = lambda (self): 1 if correct else 0


class SelectionAnswer(Base):
    __tablename__ = "answers_type_selection"
    answer_id = AnswerFK(primary_key=True)
    correct = C(BOOL, nullable=False)
    value = C(NUMERIC, default=1)


class OrderAnswer(Base):
    __tablename__ = "answers_type_order"
    answer_id = AnswerFK(primary_key=True)
    correct_position = C(INT, nullable=False)
    value = C(NUMERIC, default=1)  # Todo: default = lambda (self): 1 if correct else 0


class ShortAnswer(Base):
    __tablename__ = "answers_type_short"
    answer_id = AnswerFK(primary_key=True)


class CorrectShortAnswers(Base):
    __tablename__ = "answers_type_short_answer"
    answer_id = AnswerFK(primary_key=True)
    correct = C(TEXT, nullable=False)
    value = C(NUMERIC, default=1)


class EssayAnswer(Base):
    __tablename__ = "answers_type_essay"
    answer_id = AnswerFK(primary_key=True)


class QuizSession(Base):
    __tablename__ = "quiz_sessions"
    id = ID()
    ts = TS()
    quiz_id = QuizFK()
    room_id = RoomFK()


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
    id = ID()
    ts = TS()
    quiz_session_id = QuizSessionFK()
    user_id = UserFK()


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
    question_id = QuestionFK(primary_key=True)


class QSE_Teacher_QuestionFinished(Base, _qse):
    quiz_session_event_id = QseFK(primary_key=True)
    question_id = QuestionFK(primary_key=True)


class QSE_Teacher_QuestionModified(Base, _qse):
    quiz_session_event_id = QseFK(primary_key=True)
    old_question = QuestionFK(primary_key=True)
    new_question = QuestionFK()


class QSE_Teacher_QuestionRemoved(Base, _qse):
    quiz_session_event_id = QseFK(primary_key=True)
    question_id = QuestionFK(primary_key=True)


class QSE_Teacher_AnswerAdded(Base, _qse):
    quiz_session_event_id = QseFK(primary_key=True)
    new_answer = AnswerFK(primary_key=True)


class QSE_Teacher_AnswerModified(Base, _qse):
    quiz_session_event_id = QseFK(primary_key=True)
    old_answer = AnswerFK(primary_key=True)
    new_answer = AnswerFK()


class QSE_Teacher_AnswerRemoved(Base, _qse):
    quiz_session_event_id = QseFK(primary_key=True)
    answer_id = AnswerFK(primary_key=True)


class QSE_Student_QuizStarted(Base, _qse):
    quiz_session_event_id = QseFK(primary_key=True)


class QSE_Student_QuizFinished(Base, _qse):
    quiz_session_event_id = QseFK(primary_key=True)


class QSE_Student_QuestionStarted(Base, _qse):
    quiz_session_event_id = QseFK(primary_key=True)
    question_id = QuestionFK(primary_key=True)


class QSE_Student_QuestionFinished(Base, _qse):
    quiz_session_event_id = QseFK(primary_key=True)
    question_id = QuestionFK(primary_key=True)


class QSE_Student_AnswerSelected(Base, _qse):
    quiz_session_event_id = QseFK(primary_key=True)
    # Todo: Implement human waiting period:
    #  Perhaps don't add event if more than 3 selections happen in less than .2 seconds?
    answer_id = AnswerFK(primary_key=True)


class QSE_Student_AnswerLockedIn(Base, _qse):
    quiz_session_event_id = QseFK(primary_key=True)
    answer_id = AnswerFK(primary_key=True)



