# https://fastapi.tiangolo.com/tutorial/dependencies/
from typing import Generator

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from sqlalchemy.orm import Session

from app import database, schemas
from app.core import settings, security

_reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_STR_V1}/login/access-token"
)


async def get_db() -> Generator:
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(_reusable_oauth2)
):
    payload = jwt.decode(
        token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
    )
    token_data = schemas.TokenPayload(**payload)
    return crud.user.get(db, id=token_data.sub)
