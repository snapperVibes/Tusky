import enum
from decimal import Decimal
from typing import NamedTuple, Type, Tuple, Union, Optional, Any, Dict, List

from pydantic import BaseModel, UUID4
from .pydantic_json_patch import JsonPatchRequest

from app.pydantic_json_patch.op import Op, Add, Remove, JsonOp
from app.external import Snowflake


# Design decision: Instead of each group of classes (for example, QuizCreate, QuizPatch,
# and QuizResponse) sharing a _QuizBase class, shared attributes are repeated.
# Repetition is a small price to pay for clearer code.


class CRUDSchemas(NamedTuple):
    create: Type[BaseModel]
    patch: Type[BaseModel]
    response: Type[BaseModel]


#######################################################################################
class AnswerResponse(BaseModel):
    points: Decimal = Decimal(0)
    text: str
    # index: int


class QuestionType(enum.Enum):
    # SHORT_ANSWER = ...
    # ESSAY = ...
    MULTIPLE_CHOICE = "multiple choice"


class QuestionResponse(BaseModel):
    id: Snowflake
    query: str
    type: QuestionType
    answers: Optional[List[AnswerResponse]]
    # index: int  # Index is editable but not on the object itself


class QuizCreate(BaseModel):
    owner: Snowflake  # UserID
    title: str


class QuizPatch(JsonPatchRequest):
    # Schema:
    #
    #   title: str
    #   owner: Snowflake
    #   questions: List[Question]
    #
    #   class Question(BaseModel):
    #
    pass


class QuizResponse(BaseModel):
    id: Snowflake  # Immutable
    title: str
    owner: Snowflake
    questions: List[QuestionResponse]

    class Config:
        orm_mode = True


quiz = CRUDSchemas(QuizCreate, QuizPatch, QuizResponse)


#######################################################################################
