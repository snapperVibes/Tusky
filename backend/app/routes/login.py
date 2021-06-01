# Python convention is classes are uppercase
from datetime import timedelta as TimeDelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import schemas, crud, settings, security
from . import _depends as deps
from ..exceptions import Http400InactiveUser

router = APIRouter(
    prefix="/login",
    tags=["login"],
)


@router.post("access", response_model=schemas.Token)
def login_access_token(
    db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm),
):
    """
    OAuth2 compatible token login, get an access token for future requests

    Raises: Http404UserNotFound, Http400IncorrectPassword
    """
    user = crud.user.authenticate(
        db, username=form_data.username, password=form_data.password
    )
    if not crud.user.is_active(user):
        raise Http400InactiveUser
    access_token_expires = TimeDelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    # return the token
    return {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }
