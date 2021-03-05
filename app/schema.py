""" A home for PyDantic models """
from pydantic import BaseModel, ValidationError
from pydantic.dataclasses import dataclass


class ORMModel(BaseModel):
    class Config:
        orm_mode = True


@dataclass
class Role:
    name: str
    emoji: str


class RoomDetails(ORMModel):
    code: str
    active: bool


class UserDetails(ORMModel):
    name: str
    number: int
