""" A home for PyDantic models """
from pydantic import BaseModel, ValidationError
from pydantic.dataclasses import dataclass


@dataclass
class Role:
    name: str
    emoji: str


class RoomDetails(BaseModel):
    code: str
    active: bool

    class Config:
        orm_mode = True
