import os
import random
import sys
import unicodedata
from collections import defaultdict
from typing import Optional, TypeVar, Callable, DefaultDict, Any, Generator

import motor.motor_asyncio
from bson import ObjectId
from fastapi import FastAPI, Depends
from pydantic import BaseModel, validator

_T = TypeVar("_T")


class PyObjectId(ObjectId):
    # Mongodb boilerplate representing the BSON object ID
    # https://developer.mongodb.com/quickstart/python-quickstart-fastapi/#the-_id-attribute-and-objectids
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


def declare_event(func: Callable):
    """Decorator that logs called functions to the event log"""

    # Todo: make it not return memory values
    def wrapped(*args, **kwargs):
        print(
            f"Calling {func.__name__} with arguments {args} and keyword arguments {kwargs}"
        )
        value = func(*args, **kwargs)
        print(f"Returned {value}")
        return value

    return wrapped


class Discriminator:
    __slots__ = (
        "seed",
        "position",
        "start",
        "stop",
        "assigned",
        "released",
        "next_discriminator",
    )

    @declare_event
    def __init__(
        self,
        *,
        seed: int,
        position: int,
        start: int,
        stop: int,
        assigned: Optional[list] = None,
        released: Optional[list] = None,
        next_discriminator: Optional["Discriminator"] = None,
    ):
        self.seed = seed
        self.position = 0
        self.start = start
        self.stop = stop
        self.assigned = assigned or []
        self.released = released or []
        self.next_discriminator: Optional[Discriminator] = None

    def __iter__(self):
        return self

    @declare_event
    def __next__(self):
        sequence = self.generate_sequence(k=(self.stop - self.start))
        while True:
            try:
                value = sequence[self.position]
            except IndexError:
                if self.released:
                    return self.released.pop()
                if self.next_discriminator is None:
                    raise StopIteration("The discriminator has been exhausted.")
                return self.next_discriminator.__next__()

            self.position += 1
            if value in self.assigned:
                continue
            return value

    def next(self):
        return self.__next__()

    def assign_requested_discriminator(self, d: int) -> int:
        sequence = self.generate_sequence(k=self.position)
        if d in sequence:
            for index, released_value in enumerate(self.released):
                if d == released_value:
                    return self.released.pop(index)
            raise KeyError("The discriminator has already been assigned.")
        if d in self.assigned:
            raise KeyError("The discriminator has already been assigned.")
        self.assigned.append(d)
        return d

    def release_requested_discriminator(self, d: int) -> int:
        if d in self.released:
            raise KeyError("The value has already been released")
        sequence = self.generate_sequence(k=self.position)
        if d in sequence:
            self.released.append(d)
            return d
        for index, assigned_value in enumerate(self.assigned):
            if d == assigned_value:
                return self.assigned.pop(index)
        raise KeyError("The discriminator has not been")

    def generate_sequence(self, k: int):
        original_state = random.getstate()
        random.seed(self.seed, version=2)
        _range = range(self.start, self.stop)
        sequence = random.sample(_range, k)
        random.setstate(original_state)
        return sequence

    def to_dict(
        self,
    ):
        return {
            "seed": self.seed,
            "position": self.position,
            "start": self._range.start,
            "stop": self._range.stop,
            "assigned": self.assigned,
            "released": self.released,
            "next_discriminator": self.next_discriminator,
        }


def to_identifier(text: str) -> str:
    """Normalizes utf-8 strings using normalization form KD and lowercase characters"""
    # https://unicode.org/reports/tr15/
    #   For each character, there are two normal forms: normal form C and normal form D.
    #   Normal form D (NFD) is also known as canonical decomposition,
    #   and translates each character into its decomposed form.
    #   Normal form C (NFC) first applies a canonical decomposition,
    #   then composes pre-combined characters again...
    #   The normal form KD (NFKD) will apply the compatibility decomposition,
    #   i.e. replace all compatibility characters with their equivalents.
    name = unicodedata.normalize("NFKD", text).lower()
    if len(text) < 2:
        raise ValueError("The normalized text must be at least 2 characters long")
    if ("#" in text) or ("@" in text):
        raise ValueError("The normalized text cannot contain the characters '@' or '#'")
    return name


DiscriminatorDB = Any


async def get_db() -> Generator[DiscriminatorDB, Any, None]:
    """Dependency injection pattern used by FastAPI to yield access to the database.
    The pattern is used here to make transition to a "real" database simpler in the future."""
    client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
    yield client.discriminator


class DiscriminatorRequest(BaseModel):
    string: str
    value: Optional[int]

    @validator("string")
    def to_identifier(cls, v):
        return to_identifier(v)

    @validator("value")
    def not_null(cls, v):
        """Field is optional, but if present must not be null"""
        if v is None:
            raise ValueError
        return v


class UnlinkRequest(BaseModel):
    string: str
    value: int

    @validator("string")
    def to_identifier(cls, v):
        return to_identifier(v)


class DiscriminatorResponse(BaseModel):
    value: int


app = FastAPI()


@app.post("/discriminator/request", response_model=DiscriminatorResponse)
async def request_discriminator(
    *,
    db: DiscriminatorDB = Depends(get_db),
    request_in: DiscriminatorRequest,
):
    db_obj = await db[request_in.string].insert_one({"ok": 1})
    print(db_obj)


@app.post("/discriminator/unlink", response_model=DiscriminatorResponse)
async def unlink_discriminator(
    *, db: DiscriminatorDB = Depends(get_db), request_in: UnlinkRequest
):
    # discriminator = db[request_in.string]
    # v = discriminator.release_requested_discriminator(request_in.value)
    # return DiscriminatorResponse(value=v)
    pass


if __name__ == "__main__":
    # For degbugging
    import uvicorn

    uvicorn.run("__init__:app", port=8000, reload=True)
