# CheckConstraint validates at the database level
# Validate validates at the Model level
# fmt: off  | It's on you to maintain formatting (Todo: snapfmt)
import enum
import time
from functools import cache
from typing import Optional

from sqlalchemy import (
    BLOB,
    BOOLEAN as BOOL,
    CheckConstraint,
    Column as C,
    DATETIME,
    ForeignKey as FK,
    Identity as IDENTITY,
    INT,
    TEXT,
    VARCHAR,
    UniqueConstraint,
    NUMERIC,
)
from sqlalchemy.sql import functions
from sqlalchemy.orm import validates

from .db import Base


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
def QuestionFK(): return C(INT, FK("question.id"), nullable=False)
def AnswerFK():   return C(INT, FK("answer.id"), nullable=False)
def ImageFK():    return C(INT, FK("image.id"), nullable=False)


# fmt: on
########################################################################################
# Models
# Todo: Choose naming schema
class Users(Base):
    # User names must be between 1 and 32 characters long
    id          = ID()
    creation_ts = TS()
    name        = C(VARCHAR(32), CheckConstraint(min_size("name", 1), nullable=False))
    salt        = C(TEXT, nullable=False)
    password    = C(TEXT, nullable=False)

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
    user         = C(INT, FK("users.id"), primary_key=True)
    emailaddress = C(INT, FK("emailaddresses.id"), primary_key=True)
    visibility   = C()  # Todo: Email visibility


class Roles(Base):
    id          = ID()
    creation_ts = TS()
    name        = C(TEXT, nullable=False, unique=True)
    description = C(TEXT)


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
    code  = C(TEXT)
    valid = C(BOOL)


class UserEvent(Base):
    user        = C(INT)
    creation_ts = TS()


class Quizzes(Base):
    id          = ID()
    creation_ts = TS()


class AnswerType(enum.Enum):
    RADIO     = "Radio"  # Only one answer of type Radio can be correct per question
    SELECTION = "Selection"  # 0 or more answers of type selection can be selected
    ORDER     = "Order"  # Draggable answer whose correctness is decided by its position
    #  relative to the other answers
    RESPONSE  = "Response"  # User response.
    # Todo: Sub categorize into two types: SHORT RESPONSE and ESSAY, where short response has selected answers and essay is on the teacher to grade.


class Question(Base):
    id          = ID()
    creation_ts = TS()
    type        = C(QuestionType, nullable=False)
    quiz_id     = C(INT, FK("quizzes.id"))
    image       = C(INT, FK("images.id"))


class Answer(Base):
    id = ID()
    creation_ts     = TS()
    question_id     = QuestionFK()
    identifier      = C(TEXT)
    # Todo: Add validation that ensures two answers on the same question can't have the same order
    # Todo: Ensure order starts at 1 and every gap is filled
    order           = C(INT, nullable=False)
    image           = C(INT, FK("images.id"))
    correct         = C(BOOL, nullable=False)
    positive_points = C(NUMERIC, default=1)
    negative_points = C(NUMERIC, default=0)


class UploadedImages(Base):
    id          = ID()
    creation_ts = TS()
    data        = C(BLOB, nullable=False)
    description = C(TEXT)


class LinkUsersAndQuizes(Base):
    pass


# class RoleScope(enum.Enum):
#     Global = 1
#     Room = 2
#
#
# class LinkUsersAndRoles(Base):
#     __tablename__ = "link_users_userroles"
#     user = C(INT, FK("users.id"), primary_key=True)
########################################################################################
# Quiz Session and related tables
# Todo: NAMING
class QuizSession(Base):
    """"""
    id          = ID()
    creation_ts = TS()
    quiz_id     = C(INT, FK("quizzes.id"), nullable=False)
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
    #   UserRole: SuperAdmin, Admin, Plebeian PLEBEIAN
    #   EntityType: Quiz, Question, Answer
    #   Action: Started, Finished, Added, Modified (Requires old and new), Selected, locked-in Removed,


class QuizSessionEventType(enum.Enum):
    # We purposefully do not give Admins the ability to add questions mid quiz
    # Adding questions mid quiz seems like a good way for things to fall apart
    # Todo: Define order taxonomy for copy-editors.
    #  (Coders shouldn't have to worry about it.)
    #       SuperAdmin, Admin, Plebeian PLEBEIAN
    #       Quiz, Question, Answer
    #       Started, Finished, Added, Modified (Requires old and new), Selected, locked-in Removed,
    ADMIN_QUIZ_STARTED         = "Quiz started"
    ADMIN_QUIZ_FINISHED        = "Quiz finished"
    ADMIN_QUESTION_STARTED     = "Question started"
    ADMIN_QUESTION_FINISHED    = "Question finished"
    ADMIN_QUESTION_MODIFIED    = "Question modified"
    ADMIN_QUESTION_REMOVED     = "Question removed"
    ADMIN_ANSWER_ADDED         = "Answer added"
    ADMIN_ANSWER_MODIFIED      = "Answer modified"
    ADMIN_ANSWER_REMOVED       = "Answer removed"
    PLEBEIAN_QUIZ_STARTED      = "Quiz started"
    PLEBEIAN_QUIZ_FINISHED     = "Quiz finished"
    PLEBEIAN_QUESTION_STARTED  = "Question started"
    PLEBEIAN_QUESTION_Finished = "Question finished"
    PLEBEIAN_ANSWER_SELECTED   = "Answer selected"
    PLEBEIAN_ANSWER_LOCKED_IN  = "Answer locked in"


class _QuizSessionEventType:
    """ Common attributes for every quiz_session_event table"""
    id                    = ID()
    creation_ts           = TS()
    quiz_session_event_id = C(INT, FK("quiz_session_event.id"), nullable=False)
    user_id               = C(INT, FK("users.id"), nullable=False)


class QSE_Admin_QuizStarted(Base, _QuizSessionEventType):
    """"""


class QSE_Admin_QuizFinished(Base, _QuizSessionEventType):
    """"""


class QSE_Admin_QuestionStarted(Base, _QuizSessionEventType):
    # Todo: Validation that you can't start the same question twice before finishing it
    question_id = QuestionFK()


class QSE_Admin_QuestionFinished(Base, _QuizSessionEventType):
    question_id = QuestionFK()


class QSE_Admin_QuestionModified(Base, _QuizSessionEventType):
    old_question = QuestionFK()
    new_question = QuestionFK()


class QSE_Admin_QuestionRemoved(Base, _QuizSessionEventType):
    question_id = QuestionFK()


class QSE_Admin_AnswerAdded(Base, _QuizSessionEventType):
    new_answer = AnswerFK()


class QSE_Admin_AnswerModified(Base, _QuizSessionEventType):
    old_answer = AnswerFK()
    new_answer = AnswerFK()


class QSE_Admin_AnswerRemoved(Base, _QuizSessionEventType):
    answer_id = AnswerFK()


class QSE_Plebeian_QuizStarted(Base, _QuizSessionEventType):
    """"""


class QSE_Plebeian_QuizFinished(Base, _QuizSessionEventType):
    """"""


class QSE_Plebian_QuestionStarted(Base, _QuizSessionEventType):
    question_id = QuestionFK()


class QSE_Plebian_QuestionFinished(Base, _QuizSessionEventType):
    question_id = QuestionFK()


class QSE_Plebiean_AnswerSelected(Base, _QuizSessionEventType):
    # Todo: Implement human waiting period:
    #  Perhaps don't add event if more than 3 selections happen in less than .2 seconds?
    answer_id = AnswerFK()


class QSE_Plebiean_AnswerLockedIn(Base, _QuizSessionEventType):
    answer_id = AnswerFK()


# fmt: on
