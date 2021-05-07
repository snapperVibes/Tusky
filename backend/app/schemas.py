# SECURITY NOTE:
#   Schemas _XyzBase and XyzUpdate CAN NOT have properties that would break things
#   if the updated property is not the same as the original property
#   without the schema also inheriting the LoginRequired mixin.
#   At the time of writing, THE MIXIN IS NOT YET IMPLEMENTED
import random
import string
from functools import partial
from typing import Optional, List

from pydantic import BaseModel, validator, Field
from uuid import UUID


def _sort_by_id(_list: List, on: str):
    # Todo: This function isn't optimized.
    copied_list = _list.copy()
    sorted_list = []
    # Modifying the original list seems sketchy, so we create a copy

    def _sort(remaining_list: List, prev_id: Optional[int]):
        for index, value in enumerate(remaining_list):
            if getattr(value, on) == prev_id:
                sorted_list.append(remaining_list[index])
                return _sort(remaining_list, prev_id=value.id)

    _sort(copied_list, prev_id=None)
    return sorted_list


_sort_questions = partial(_sort_by_id, on="previous_question")
_sort_answers = partial(_sort_by_id, on="previous_answer")

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
# class XyzPublic(_XyzBase):
#     """ Additional properties to return via API """
#
#
# class XyzInDB(_XyzInDBBase):
#     """ Additional properties stored in the database """
#
#
########################################################################################
# Todo: Write logic 😛
class LoginRequired:
    pass


########################################################################################
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    # subject
    sub: Optional[UUID] = None


########################################################################################
class _UserBase(BaseModel):
    display_name: Optional[str] = None
    is_active: Optional[bool] = True
    # Todo: Secure is_superuser
    is_superuser: bool = False


class UserCreate(_UserBase):
    display_name: str
    password: str


class UserUpdate(_UserBase, LoginRequired):
    number: int  # Todo: Type: UserNumber
    password: Optional[int] = None
    number: int = None


class _UserInDBBase(_UserBase):
    id: Optional[UUID] = None
    identifier_name: str
    number: int

    @validator("number")
    def display_number(cls, v):
        # 1 -> "0051", 10245 -> "10245"
        return str(v).zfill(4)

    class Config:
        orm_mode = True


class UserPublic(_UserInDBBase):
    pass


class UserInDB(_UserInDBBase):
    hashed_password: str


########################################################################################
class _RoomBase(BaseModel):
    is_active: Optional[bool] = True
    # Todo: Add url property (Pydantic HttpUrl)


class RoomCreate(_RoomBase, LoginRequired):
    owner_id: UUID
    code: str = Field(
        default_factory=lambda: "".join(
            random.choice(string.ascii_uppercase) for _ in range(5)
        )
    )


class RoomUpdate(_RoomBase, LoginRequired):
    # Room events. Do these belong in a different area?
    id: UUID


class _RoomInDBBase(_RoomBase):
    id: UUID
    owner_id: UUID
    code: str

    class Config:
        orm_mode = True


class RoomPublic(_RoomInDBBase):
    pass


class RoomInDB(_RoomInDBBase):
    pass


########################################################################################
class _AnswerBase(BaseModel):
    text: str


class AnswerCreate(_AnswerBase, LoginRequired):
    pass


class AnswerUpdate(_AnswerBase, LoginRequired):
    pass


class _AnswerInDBBase(_AnswerBase):
    id: UUID
    previous_answer: Optional[UUID]

    class Config:
        orm_mode = True


class AnswerPublic(_AnswerInDBBase):
    pass


########################################################################################
class _QuestionBase(BaseModel):
    query: str


class QuestionCreate(_QuestionBase, LoginRequired):
    answers: List[AnswerCreate]
    previous_question: Optional[UUID] = None


class QuestionUpdate(_QuestionBase, LoginRequired):
    previous_question: Optional[UUID] = None


class _QuestionInDBBase(_QuestionBase):
    id: Optional[UUID] = None
    previous_question: Optional[UUID]
    answers: List[AnswerPublic]

    @validator("answers")
    def sort_answers(cls, v):
        return _sort_answers(v)

    class Config:
        orm_mode = True


class QuestionPublic(_QuestionInDBBase):
    pass


########################################################################################
class _QuizBase(BaseModel):
    # Todo: Verify length of 1
    name: str


class QuizPreview(BaseModel):
    id: UUID
    owner: UUID


class QuizCreate(_QuizBase, LoginRequired):
    # Todo: Figure out how to sync Create/Update
    owner: UUID = Field(alias="owner_id")
    questions: Optional[List[QuestionCreate]]


class QuizUpdate(_QuizBase, LoginRequired):
    # Todo: Figure out how to sync Create/Update
    id: UUID
    owner: UUID = Field(alias="owner_id")
    questions: Optional[List[QuestionCreate]]


class _QuizInDBBase(_QuizBase):
    id: Optional[UUID] = None
    owner: UUID = Field(alias="owner_id")
    questions: List[QuestionPublic]

    @validator("questions")
    def sort_questions(cls, v):
        return _sort_questions(v)

    class Config:
        orm_mode = True


class QuizPublic(_QuizInDBBase):
    pass
