from typing import Optional, Any

from pydantic import BaseModel, EmailStr, validator
from uuid import UUID


# # Template
# #
# class _XyzBase(BaseModel):
#     """ Shared properties """
#
#
# class XyzCreate(_XyzBase):
#     """ Properties to receive via API on creation """
#
#
# class XyzUpdate(_XyzBase):
#     """ Properties to receive via API on update"""
#     # Should these have close methods that alias to set_active = False?
#
#
# class _XyzInDBBase(_XyzBase):
#     class Config:
#         orm_mode = True
#
#
# class Xyz(_XyzBase):
#     """ Additional properties to return  via API """
#
#
# class XyzInDB(_XyzInDBBase):
#     """ Additional properties stored in the database """
#
#
########################################################################################
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    sub: Optional[UUID] = None


########################################################################################
class _UserBase(BaseModel):
    display_name: Optional[str] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False


class UserCreate(_UserBase):
    display_name: str
    password: str


class UserUpdate(_UserBase):
    number: int  # Todo: Type: UserNumber
    password: Optional[int] = None
    number: int = None


class _UserInDBBase(_UserBase):
    id: Optional[UUID] = None
    identifier_name: str
    number: int

    @validator("number")
    def display_number(cls, v, values):
        if int(v) < 1:
            if values["display_name"] != "admin":
                raise ValueError("Number must be greater than or equal to one.")
        # 1 -> "0051", 10245 -> "10245"
        return str(v).zfill(4)

    class Config:
        orm_mode = True


class User(_UserInDBBase):
    pass


class UserInDB(_UserInDBBase):
    hashed_password: str


########################################################################################
class _RoomBase(BaseModel):
    is_active: Optional[bool] = True


class RoomCreate(_RoomBase):
    code: Optional[str] = None


class RoomUpdate(_RoomBase):
    # Room events. Do these belong in a different area?

    # The quiz url. Todo: Pydantic probably has a url type
    start_quiz: Optional[str] = None


class _RoomInDBBase(_RoomBase):
    id: Optional[UUID] = None

    class Config:
        orm_mode = True


class Room(_RoomInDBBase):
    pass


class RoomInDB(_RoomInDBBase):
    pass


########################################################################################
class _QuizBase(BaseModel):
    name: str
    owner: str


class QuizCreate(_QuizBase):
    pass


class QuizUpdate(_QuizBase):
    pass


class _QuizInDBBase(_QuizBase):
    id: Optional[UUID] = None

    class Config:
        orm_mode = True


class Quiz(_QuizInDBBase):
    pass


class QuizInDB(_QuizInDBBase):
    pass


########################################################################################
class _QuestionBase(BaseModel):
    query: str
    quiz_name: str
    owner_name: str


class QuestionCreate(_QuestionBase):
    pass


class QuestionUpdate(_QuestionBase):
    pass


class _QuestionInDBBase(_QuestionBase):
    id: Optional[UUID] = None

    class Config:
        orm_mode = True


class Question(_QuestionInDBBase):
    pass


class QuestionInDB(_QuestionInDBBase):
    pass
