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
    identifier_name: Optional[str] = None
    display_name: Optional[str] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False

    # @validator("identifier_name")
    # def ensure_identifier_or_display_name(cls, v, values):
    #     # https://github.com/samuelcolvin/pydantic/issues/506#issuecomment-522255484
    #     if "display_name" not in values and not v:
    #         raise ValueError(
    #             "At least one of 'display_name' or 'identifier_name' must be provided"
    #         )

    # @validator("identifier_name", "display_name")
    # def name_length_between_1_and_32_characters(cls, v):
    #     if not 1 <= len(v) <= 32:
    #         raise ValueError("Name length must be between 1 and 32 characters")
    #     return v
    #
    # @validator("identifier_name", "display_name")
    # def name_does_not_contain_hash_symbol(cls, v):
    #     if "#" in v:
    #         raise ValueError("Name must not contain the hash symbol '#")
    #     return v

class UserCreate(_UserBase):
    display_name: str
    password: str


class UserUpdate(_UserBase):
    number: int  # Todo: Type: UserNumber
    password: Optional[int] = None
    number: int = None



class _UserInDBBase(_UserBase):
    id: Optional[UUID] = None
    number: int

    @validator("number")
    def display_number(cls, v):
        if int(v) < 1:
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
    pass  # Todo: If there aren't additional properties, remove


########################################################################################
class _QuizBase(BaseModel):
    name: Optional[str]


class QuizCreate:
    name: str


class _QuizInDBBase(_QuizBase):
    id: Optional[UUID] = None

    class Config:
        orm_mode = True


class Quiz(_QuizInDBBase):
    pass
