# Lifted directly from fastapi-users documentation
# https://frankie567.github.io/fastapi-users/configuration/full-example.html
import unicodedata
from typing import Optional

import databases
import sqlalchemy
from fastapi import FastAPI, Request
from fastapi_operation_id import clean_ids
from fastapi_users import FastAPIUsers, models
from fastapi_users.authentication import JWTAuthentication
from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from pydantic import BaseModel, validator
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base

DATABASE_URL = "sqlite:///./users.db"
SECRET = "SECRET"


class TuskyUser(BaseModel):
    id_name: Optional[str]
    display_name: Optional[str]

    @validator("display_name")
    def normalize_name(cls, v, values):
        """Normalizes utf-8 strings using normalization form KD and lowercase characters"""
        # https://unicode.org/reports/tr15/
        #   For each character, there are two normal forms: normal form C and normal form D.
        #   Normal form D (NFD) is also known as canonical decomposition,
        #   and translates each character into its decomposed form.
        #   Normal form C (NFC) first applies a canonical decomposition,
        #   then composes pre-combined characters again...
        #   The normal form KD (NFKD) will apply the compatibility decomposition,
        #   i.e. replace all compatibility characters with their equivalents.
        name = unicodedata.normalize("NFKD", values["id_name"]).lower()
        if "#" in name:
            raise
        return name


class User(models.BaseUser, TuskyUser):
    pass


class UserCreate(models.BaseUserCreate):
    display_name: str


class UserUpdate(User, models.BaseUserUpdate):
    pass


class UserDB(User, models.BaseUserDB):
    pass


database = databases.Database(DATABASE_URL)
Base: DeclarativeMeta = declarative_base()


class UserTable(Base, SQLAlchemyBaseUserTable):
    pass


engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
Base.metadata.create_all(engine)

users = UserTable.__table__
user_db = SQLAlchemyUserDatabase(UserDB, database, users)


def on_after_register(user: UserDB, request: Request):
    print(f"User {user.id} has registered.")


def on_after_forgot_password(user: UserDB, token: str, request: Request):
    # Email user their forgotten password
    print(f"User {user.id} has forgot their password. Reset token: {token}")


def after_verification_request(user: UserDB, token: str, request: Request):
    print(f"Verification requested for user {user.id}. Verification token: {token}")


jwt_authentication = JWTAuthentication(
    secret=SECRET, lifetime_seconds=3600, tokenUrl="auth/jwt/login"
)

app = FastAPI(title="Users")
fastapi_users = FastAPIUsers(
    user_db,
    [jwt_authentication],
    User,
    UserCreate,
    UserUpdate,
    UserDB,
)
app.include_router(
    fastapi_users.get_auth_router(jwt_authentication), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(on_after_register), prefix="/auth", tags=["auth"]
)
app.include_router(
    fastapi_users.get_reset_password_router(
        SECRET, after_forgot_password=on_after_forgot_password
    ),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(
        SECRET, after_verification_request=after_verification_request
    ),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(fastapi_users.get_users_router(), prefix="/users", tags=["users"])


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


clean_ids(app)
