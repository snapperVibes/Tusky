# CheckConstraint validates at the database level
# Validate validates at the Model level
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
# Factory functions for common columns
# fmt: off
def ID(): return C(INT, IDENTITY(), primary_key=True)
def TS(): return C(DATETIME, default=functions.now)


# fmt: on
########################################################################################
# Models
# Todo: Choose naming schema
class Users(Base):
    # User names must be between 1 and 32 characters long
    id = ID()
    creation_ts = TS()
    name = C(VARCHAR(32), CheckConstraint(min_size("name", 1), nullable=False))
    salt = C(TEXT, nullable=False)
    password = C(TEXT, nullable=False)

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
    id = ID()
    creation_ts = TS()
    # Todo: Email validation
    local = C(VARCHAR(64), CheckConstraint(min_size("local", 1)), nullable=False)
    domain = C(VARCHAR(255), CheckConstraint(min_size("domain", 1)), nullable=False)
    verified = C(bool)
    verifiedts = C(DATETIME)

    UniqueConstraint("local", "domain")


class LinkUsersAndEmailAddresses(Base):
    __tablename__ = "link_users_emailaddresses"
    user = C(INT, FK("user.id"), primary_key=True)
    emailaddress = C(INT, FK("emailaddresses.id"), primary_key=True)
    visibility = C()    # Todo: Email visibility


class Roles(Base):
    __tablename__ = "adminstrative_roles"
    id = ID()
    creation_ts = TS()
    name = C(TEXT, nullable=False, unique=True)
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
    code = C(TEXT)
    valid = C(BOOL)


class UserEvent(Base):
    user = C(INT)
    ts = C(DATETIME, default=functions.now())


class Quizzes(Base):
    id = ID()
    creation_ts = TS()


class Question(Base):
    id = ID()
    creation_ts = TS()
    quiz_id = C(INT, FK("quizzes.id"))
    text = C(TEXT, nullable=False)
    image = C(BLOB)


class UploadedImages(Base):
    id = ID()
    creation_ts = TS()
    data = C(BLOB, nullable=False)
    description = C(TEXT)


class QuizSession(Base):
    pass


class LinkUsersAndQuizes(Base):
    pass


# class RoleScope(enum.Enum):
#     Global = 1
#     Room = 2
#
#
# class LinkUsersAndRoles(Base):
#     __tablename__ = "link_users_userroles"
#     user = C(INT, FK("user.id"), primary_key=True)
