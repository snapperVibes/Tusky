# CheckConstraint validates at the database level
# Validate validates at the Model level
# fmt: off  | It's on you to maintain formatting (Todo: snapfmt)
import enum


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
    user         = C(INT, FK("users.id"), primary_key=True)
    emailaddress = C(INT, FK("emailaddresses.id"), primary_key=True)
    visibility   = C()  # Todo: Email visibility


class Rooms(Base):
    # Todo: Consider using Redis for storing ephemeral details of rooms
    id          = ID()
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
    code      = C(TEXT)
    valid     = C(BOOL)


class RoomRole(enum.Enum):
    TEACHER = Role("Teacher", "🧑‍🏫")    # Zero-width join
    STUDENT = Role("Student", "🧑‍🎓")    # Zero-width join


class Quizzes(Base):
    id          = ID()
    creation_ts = TS()


class Question(Base):
    id          = ID()
    creation_ts = TS()
    quiz_id     = QuizFK()
    image       = ImageFK()


class AnswerType(enum.Enum):
    RADIO     = "Radio"  # Only one answer of type Radio can be correct per question
    SELECTION = "Selection"  # 0 or more answers of type selection can be selected
    ORDER     = "Order"  # Draggable answer whose correctness is decided by its position
    #  relative to the other answers
    RESPONSE  = "Response"  # User response.
    # Todo: Sub categorize into two types: SHORT RESPONSE and ESSAY, where short response has selected answers and essay is on the teacher to grade.


class Answer(Base):
    id              = ID()
    creation_ts     = TS()
    question_id     = QuestionFK()
    type            = C(AnswerType, nullable=False)
    details         = FK
    identifier      = C(TEXT)
    # Todo: Add validation that ensures two answers on the same question can't have the same order
    # Todo: Ensure order starts at 1 and every gap is filled
    order           = C(INT, nullable=False)
    image           = ImageFK()
    correct         = C(BOOL, nullable=False)
    positive_points = C(NUMERIC, default=1, nullable=False)
    negative_points = C(NUMERIC, default=0, nullable=False)


class UploadedImages(Base):
    id          = ID()
    creation_ts = TS()
    data        = C(BLOB, nullable=False)
    description = C(TEXT)



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
    #   UserRole: SuperAdmin, Admin, Plebeian PLEBEIAN
    #   EntityType: Quiz, Question, Answer
    #   Action: Started, Finished, Added, Modified (Requires old and new), Selected, locked-in Removed,
    id                    = ID()
    creation_ts           = TS()
    user_id               = C(INT, FK("users.id"), nullable=False)


class QuizSessionEventType(enum.Enum):
    # We purposefully do not give Admins the ability to add questions mid quiz
    # Adding questions mid quiz seems like a good way for things to fall apart
    # Todo: Define order taxonomy for copy-editors.
    #  (Coders shouldn't have to worry about it.)
    #       Teacher, Student
    #       Quiz, Question, Answer
    #       Started, Finished, Added, Modified (Requires old and new), Selected, locked-in Removed,
    TEACHER_QUIZ_STARTED      = "Quiz started"
    TEACHER_QUIZ_FINISHED     = "Quiz finished"
    TEACHER_QUESTION_STARTED  = "Question started"
    TEACHER_QUESTION_FINISHED = "Question finished"
    TEACHER_QUESTION_MODIFIED = "Question modified"
    TEACHER_QUESTION_REMOVED  = "Question removed"
    TEACHER_ANSWER_ADDED      = "Answer added"
    TEACHER_ANSWER_MODIFIED   = "Answer modified"
    TEACHER_ANSWER_REMOVED    = "Answer removed"
    STUDENT_QUIZ_STARTED      = "Quiz started"
    STUDENT_QUIZ_FINISHED     = "Quiz finished"
    STUDENT_QUESTION_STARTED  = "Question started"
    STUDENT_QUESTION_Finished = "Question finished"
    STUDENT_ANSWER_SELECTED   = "Answer selected"
    STUDENT_ANSWER_LOCKED_IN  = "Answer locked in"


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
