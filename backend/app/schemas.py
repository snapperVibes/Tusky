import random
import string
from datetime import datetime as DateTime
from functools import partial
from typing import Optional, List

from pydantic import BaseModel, validator, Field
from uuid import UUID


def _sort_by_id(_list: List, on: str):
    # Todo: This function isn't optimized.
    # Modifying the original list seems sketchy, so we create a copy
    copied_list = _list.copy()
    sorted_list = []

    def _sort(remaining_list: List, prev_id: Optional[int]):
        for index, value in enumerate(remaining_list):
            if getattr(value, on) == prev_id:
                sorted_list.append(remaining_list.pop(index))
                return _sort(remaining_list, prev_id=value.id)

    _sort(copied_list, prev_id=None)
    assert len(sorted_list) == len(
        _list
    ), "Could not sort; Do multiple elements share the same previous element?"
    return sorted_list


_sort_questions = partial(_sort_by_id, on="previous_question")
_sort_answers = partial(_sort_by_id, on="previous_answer")


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
class StudentResponseCreate(BaseModel):
    quiz_session_id: UUID
    student_id: UUID
    question_id: UUID
    is_correct: bool


class StudentResponseUpdate(BaseModel):
    # Todo: Figure out how to make Not Implemented
    pass


class _StudentResponseInDB(BaseModel):
    quiz_session_id: UUID
    student_id: UUID
    question_id: UUID
    is_correct: bool
    ts: DateTime

    class Config:
        orm_mode = True


class StudentResponse(_StudentResponseInDB):
    pass


########################################################################################
class _AnswerBase(BaseModel):
    previous_answer: Optional[UUID]


class AnswerCreate(_AnswerBase):
    text: str
    question_id: UUID
    is_correct: bool = False


class AnswerUpdate(_AnswerBase):
    id: UUID
    text: Optional[str]
    is_correct: Optional[bool]


class _AnswerInDB(_AnswerBase):
    id: UUID
    text: str
    question_id: UUID

    class Config:
        orm_mode = True


class AnswerForStudent(_AnswerInDB):
    pass


class Answer(_AnswerInDB):
    is_correct: bool


########################################################################################
class _QuestionBase(BaseModel):
    previous_question: Optional[UUID]


class QuestionCreate(_QuestionBase):
    query: str
    quiz_id: UUID


class QuestionUpdate(_QuestionBase):
    id: UUID
    query: Optional[str]


class _QuestionInDB(_QuestionBase):
    id: UUID = None
    query: str
    quiz_id: UUID

    @validator("answers", check_fields=False)
    def sort_answers(cls, v):
        return _sort_answers(v)

    class Config:
        orm_mode = True


class QuestionForStudent(_QuestionInDB):
    answers: List[AnswerForStudent]


class Question(_QuestionInDB):
    answers: List[Answer]


########################################################################################
class QuizCreate(BaseModel):
    title: str
    owner_id: UUID


class QuizUpdate(BaseModel):
    id: UUID
    title: Optional[str]
    owner_id: Optional[UUID]


class _QuizInDB(BaseModel):
    id: UUID
    title: str
    owner_id: UUID

    @validator("questions", check_fields=False)
    def sort_questions(cls, v):
        return _sort_questions(v)

    class Config:
        orm_mode = True


class QuizPreview(_QuizInDB):
    pass


class QuizForStudent(_QuizInDB):
    questions: List[QuestionForStudent]


class Quiz(_QuizInDB):
    questions: List[Question]


########################################################################################
class QuizSessionCreate(BaseModel):
    room_id: UUID
    quiz_id: UUID
    is_active: Optional[bool] = True


class QuizSessionUpdate(BaseModel):
    id: UUID
    is_active: Optional[bool]


class _QuizSessionInDB(BaseModel):
    id: UUID
    room_id: UUID
    quiz_id: UUID
    is_active: bool

    class Config:
        orm_mode = True


class QuizSession(_QuizSessionInDB):
    pass


class QuizSessionForStudent(_QuizSessionInDB):
    quiz: Optional[QuizForStudent]


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
    session_ids: List[Optional[QuizSession]] = Field(..., alias="session")

    class Config:
        orm_mode = True


class Room(_RoomInDB):
    pass
