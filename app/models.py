# CheckConstraint validates at the database level
# Validate validates at the Model level
# fmt: off  | It's on you to maintain formatting (Todo: snapfmt)
import enum
from dataclasses import dataclass
from typing import List

from sqlalchemy import (
    BLOB,
    BOOLEAN as BOOL,
    CheckConstraint,
    Column as C,
    DATETIME,
    ForeignKey as FK,
    Identity as IDENTITY,
    INT,
    NUMERIC,
    TEXT,
    VARCHAR,
    PrimaryKeyConstraint,
    UniqueConstraint,
)
from sqlalchemy.sql import functions
from sqlalchemy.orm import validates

from .db import Base
from .types import Role


########################################################################################
# Constraints
# Todo: I'm fairly certain functions.char_length can be used somehow
#  instead of this wrapper. Figure it out
#  This whole function smells.
def min_size(column: str, minimum) -> str:
    # CHAR_LENGTH is a built-in postgres string function
    # https://www.postgresql.org/docs/13/functions-string.html#FUNCTIONS-STRING-OTHER
    return f"CHAR_LENGTH({column} >= {minimum};)"


########################################################################################
# Factory functions for common columns to ease typing and reading of repeated text

def ID():         return C(INT, IDENTITY(), primary_key=True)
def TS():         return C(DATETIME, default=functions.now)
def UserFK():     return C(INT, FK("users.id"), nullable=False)
def QseFK():      return C(INT, FK("quiz_session_event.id"), nullable=False)
def QuizFK():     return C(INT, FK("quizzes.id"), nullable=False)
def QuestionFK(): return C(INT, FK("questions.id"), nullable=False)
def AnswerFK():   return C(INT, FK("answers.id"), nullable=False)
def ImageFK():    return C(INT, FK("images.id"), nullable=False)


########################################################################################
# Models
# The database is normalized to a reasonable level.
# Todo: Choose naming schema
class SiteRole(enum.Enum):
    SUPER_ADMIN = Role("Super Admin", "🦸")
    ADMIN       = Role("Admin", "👑")
    PLEBEIAN    = Role("User", "🙂")


class Users(Base):
    # User names must be between 1 and 32 characters long
    id          = ID()
    creation_ts = TS()
    name        = C(VARCHAR(32), CheckConstraint(min_size("name", 1), nullable=False))
    salt        = C(TEXT, nullable=False)
    password    = C(TEXT, nullable=False)
    site_role   = C(SiteRole, nullable=False)

    UniqueConstraint("name", "number")

    @validates("name")
    def validate_name(self, _, name) -> str:
        if 1 <= len("name"):
            return name
        raise ValueError("User name must be between 1 and 32 characters.")


class EmailAddresses(Base):
    # Application Techniques for Checking and Transformation of Names:
    #   https://tools.ietf.org/html/rfc3696
    __tablename__ = "emailaddresses"
    id          = ID()
    creation_ts = TS()
    # Todo: Email validation
    local       = C(VARCHAR(64), CheckConstraint(min_size("local", 1)), nullable=False)
    domain      = C(VARCHAR(255), CheckConstraint(min_size("domain", 1)), nullable=False)
    verified    = C(bool)
    verifiedts  = C(DATETIME)

    UniqueConstraint("local", "domain")


class LinkUsersAndEmailAddresses(Base):
    __tablename__ = "link_users_emailaddresses"
    user         = UserFK()
    emailaddress = C(INT, FK("emailaddresses.id"), primary_key=True)
    visibility   = C()  # Todo: Email visibility
    PrimaryKeyConstraint("user")


class Images(Base):
    id          = ID()
    creation_ts = TS()
    uploaded_by = UserFK()
    filename    = C(TEXT, nullable=False)
    public_code = C(TEXT, nullable=False)  # Todo: Discuss optimal public facing name
    data        = C(BLOB, nullable=False)
    description = C(TEXT)


#######################################################################################
class Rooms(Base):
    # Todo: Consider using Redis for storing ephemeral details of rooms
    id = ID()
    creation_ts = TS()
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

    id = ID()
    creation_ts = TS()
    room_id = C(INT, FK("rooms.id"), nullable=False)


#######################################################################################
class Quizzes(Base):
    id          = ID()
    creation_ts = TS()


class Question(Base):
    id          = ID()
    creation_ts = TS()
    quiz_id     = QuizFK()
    image       = ImageFK()


class Answer(Base):
    """
    Types of Answers:
        Radio: Only one answer of type Radio can be correct per question
        Selection: 0 or more answers of type selection can be selected
        Order: Draggable answer whose correctness is decided by its position
        ShortAnswer: Student's write in answers compared to a selection of correct answers
        Essay: Teacher manually grades written responses """
    id              = ID()
    creation_ts     = TS()
    question_id     = QuestionFK()
    identifier      = C(TEXT)
    # Todo: Add validation that ensures two answers on the same question can't have the same order
    # Todo: Ensure order starts at 1 and every gap is filled
    order           = C(INT, nullable=False)
    image           = ImageFK()


class RadioAnswer(Base):
    __tablename__ = "answer_type_radio"
    answer_id = AnswerFK()
    correct = C(BOOL, nullable=False)
    value = C(NUMERIC, default=1)   # Todo: default = lambda (self): 1 if correct else 0
    PrimaryKeyConstraint("answer_id")


class SelectionAnswer(Base):
    __tablename__ = "answer_type_selection"
    answer_id = AnswerFK()
    correct = C(BOOL, nullable=False)
    value = C(NUMERIC, default=1)
    PrimaryKeyConstraint("answer_id")


class OrderAnswer(Base):
    __tablename__ = "answer_type_order"
    answer_id = AnswerFK()
    correct_position = C(INT, nullable=False)
    value = C(NUMERIC, default=1)   # Todo: default = lambda (self): 1 if correct else 0
    PrimaryKeyConstraint("answer_id")


class ShortAnswer(Base):
    __tablename__ = "answer_type_short"
    answer_id = AnswerFK()
    PrimaryKeyConstraint("answer_id")


class CorrectShortAnswers(Base):
    __tablename__ = "answer_type_short_answers"
    answer_id = AnswerFK()
    correct = C(TEXT, nullable=False)
    value = C(NUMERIC, default=1)
    PrimaryKeyConstraint("answer_id", "correct")


class EssayAnswer(Base):
    __tablename__ = "answer_type_essay"
    answer_id = AnswerFK()
    PrimaryKeyConstraint("answer_id")


class QuizSession(Base):
    id          = ID()
    creation_ts = TS()
    quiz_id     = QuizFK()
    room_id     = C(INT, FK("rooms.id"))


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
    # Order taxonomy for copy-editors (Coders shouldn't have to worry about it.)
    #   UserRole: SuperAdmin, Admin, Plebeian
    #   EntityType: Quiz, Question, Answer
    #   Action: Started, Finished, Added, Modified (Requires old and new), Selected, locked-in Removed,
    # We purposefully do not give Admins the ability to add questions mid quiz
    # Adding questions mid quiz seems like a good way for things to fall apart
    id              = ID()
    creation_ts     = TS()
    quiz_session_id = C(INT, FK("quiz_session.id"), nullable=False)
    user_id         = UserFK()

class _qse:
    """ Quiz Session Event __tablename__ mixin to reduce typing during development """
    @property
    def __tablename__(self):
        _, entity_type, action = self.__class__.__name__.split("_")
        # Split action on capital letters
        action = "".join("_" + x.lower() if x.isupper() else x for x in action)
        return f"quiz_session_event_{entity_type}_{action}"


class QSE_Teacher_QuizStarted(Base, _qse):
    quiz_session_event_id = QseFK()


class QSE_Teacher_QuizFinished(Base, _qse):
    quiz_session_event_id = QseFK()


class QSE_Teacher_QuestionStarted(Base, _qse):
    quiz_session_event_id = QseFK()
    # Todo: Validation that you can't start the same question twice before finishing it
    question_id           = QuestionFK()


class QSE_Teacher_QuestionFinished(Base, _qse):
    quiz_session_event_id = QseFK()
    question_id           = QuestionFK()


class QSE_Teacher_QuestionModified(Base, _qse):
    quiz_session_event_id = QseFK()
    old_question          = QuestionFK()
    new_question          = QuestionFK()


class QSE_Teacher_QuestionRemoved(Base, _qse):
    quiz_session_event_id = QseFK()
    question_id           = QuestionFK()


class QSE_Teacher_AnswerAdded(Base, _qse):
    quiz_session_event_id = QseFK()
    new_answer            = AnswerFK()


class QSE_Teacher_AnswerModified(Base, _qse):
    quiz_session_event_id = QseFK()
    old_answer            = AnswerFK()
    new_answer            = AnswerFK()


class QSE_Teacher_AnswerRemoved(Base, _qse):
    quiz_session_event_id = QseFK()
    answer_id             = AnswerFK()


class QSE_Student_QuizStarted(Base, _qse):
    quiz_session_event_id = QseFK()


class QSE_Student_QuizFinished(Base, _qse):
    quiz_session_event_id = QseFK()


class QSE_StudentQuestionStarted(Base, _qse):
    quiz_session_event_id = QseFK()
    question_id           = QuestionFK()


class QSE_StudentQuestionFinished(Base, _qse):
    quiz_session_event_id = QseFK()
    question_id           = QuestionFK()


class QSE_Student_AnswerSelected(Base, _qse):
    quiz_session_event_id = QseFK()
    # Todo: Implement human waiting period:
    #  Perhaps don't add event if more than 3 selections happen in less than .2 seconds?
    answer_id             = AnswerFK()


class QSE_Student_AnswerLockedIn(Base, _qse):
    quiz_session_event_id = QseFK()
    answer_id             = AnswerFK()


# fmt: on
