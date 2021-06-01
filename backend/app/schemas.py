import random
import string
from typing import Optional, List, Literal, Union, Any

import pydantic
from pydantic import BaseModel, validator, Field, Json
from uuid import UUID


# def _sort_by_id(_list: List, on: str):
#     # Todo: This function isn't optimized.
#     # Modifying the original list seems sketchy, so we create a copy
#     copied_list = _list.copy()
#     sorted_list = []
#
#     def _sort(remaining_list: List, prev_id: Optional[int]):
#         for index, value in enumerate(remaining_list):
#             if getattr(value, on) == prev_id:
#                 sorted_list.append(remaining_list.pop(index))
#                 return _sort(remaining_list, prev_id=value.id)
#
#     _sort(copied_list, prev_id=None)
#     assert len(sorted_list) == len(
#         _list
#     ), "Could not sort; Do multiple elements share the same previous element?"
#     return sorted_list
#
#
# _sort_questions = partial(_sort_by_id, on="previous_question")
# _sort_answers = partial(_sort_by_id, on="previous_answer")


########################################################################################
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    # subject
    sub: Optional[UUID] = None


########################################################################################
class UserCreate(BaseModel):
    display_name: str
    password: str
    is_active: bool = True
    is_superuser: bool = False


class UserUpdate(BaseModel):
    id: UUID
    display_name: Optional[str]
    password: Optional[str]
    is_active: Optional[bool]
    is_superuser: Optional[bool]
    number: Optional[int]  # Todo: Type: UserNumber


class _UserInDB(BaseModel):
    id: UUID
    display_name: str
    is_active: bool
    is_superuser: bool
    number: int
    identifier_name: str

    @validator("number")
    def display_number(cls, v):
        # 1 -> "0051", 10245 -> "10245"
        return str(v).zfill(4)

    class Config:
        orm_mode = True


class User(_UserInDB):
    pass


class UserInDB(_UserInDB):
    hashed_password: str


########################################################################################
class RoomCreate(BaseModel):
    owner_id: UUID
    code: str = Field(
        default_factory=lambda: "".join(
            random.choice(string.ascii_uppercase) for _ in range(5)
        )
    )
    is_active: bool = True


# Do room events go here?
class RoomUpdate(BaseModel):
    id: UUID
    code: Optional[str]
    is_active: Optional[bool]


class _RoomInDB(BaseModel):
    id: UUID
    owner_id: UUID
    code: str
    is_active: bool
    # session_ids: List[Optional[QuizSession]] = Field(..., alias="session")

    class Config:
        orm_mode = True


class Room(_RoomInDB):
    pass


########################################################################################
class AnswerChoice(BaseModel):
    text: str
    is_correct: Optional[bool] = False


class _QuestionBase(BaseModel):
    query: str
    type = str


class MultipleChoice(_QuestionBase):
    type: Literal["multiple-choice"] = "multiple-choice"
    answers: list[AnswerChoice]


class ShortAnswer(_QuestionBase):
    type: Literal["short-answer"] = "short-answer"
    answers: list[str]


AnyQuestion = Union[MultipleChoice, ShortAnswer]


class _QuizContent(BaseModel):
    t: str = Field(..., title="title")
    q: list[AnyQuestion] = Field(..., title="questions")


class QuizCreate(BaseModel):
    owner_id: UUID
    is_public: bool
    content: _QuizContent


class QuizUpdate(BaseModel):
    # This implementation is flaky.
    # If updating this schema, also update crud.CRUDQuiz
    id: UUID
    set_is_public: Optional[bool]
    patch_content: Optional[Union[Json, list[Json]]]

    @validator("set_title", "set_is_public", "patch_content")
    def not_null(cls, v):
        if v is None:
            raise ValueError
        return v
