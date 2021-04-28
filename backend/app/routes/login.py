# Python convention is classes are uppercase
from datetime import timedelta as TimeDelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import schemas, models, crud, settings, security
from . import _depends as deps


router = APIRouter(
    tags=["login"],
)


@router.get("/", include_in_schema=False)
def home():
    return {"msg": "Welcome to Tusky's API 🐘."}


@router.post("/login/access-token", response_model=schemas.Token)
def login_access_token(
    db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm),
):
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = crud.user.authenticate(
        db, username=form_data.username, password=form_data.password
    )
    # Todo: There's no point to using this if you don't actually use it correctly
    if user := user.ok():
        pass
    # Todo: This is where pattern matching is to be used
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    elif not crud.user.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = TimeDelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    # return the token
    return {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }
