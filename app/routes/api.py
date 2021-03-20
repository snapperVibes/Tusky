__all__ = ["api_router"]
from datetime import timedelta

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import settings, crud, schemas, models
from app.core import security
from app.routes import _depends as deps

#######################################################################################
# login

login_router = APIRouter()

@login_router.post("/login/access-token", response_model=schemas.Token)
def login_access_token(
    db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    name, number = form_data.username.split("#")
    user = crud.user.authenticate(
        db, username=name, number=number, password=form_data.password
    )
    # Todo: There's no point to using this if you don't actually use it correctly
    user = user.ok()
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not crud.user.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


#######################################################################################
# rooms
rooms_router = APIRouter()


#######################################################################################
# users
users_router = APIRouter()

@users_router.post("/create", response_model=schemas.User)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_init: schemas.UserCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser)
):
    user = crud.user.create(db, obj_init=user_init)
    return user


@users_router.get("/me", response_model=schemas.User)
def read_current_user(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    return current_user


#######################################################################################
api_router = APIRouter()
api_router.include_router(login_router, prefix=settings.API_V1_STR, tags=["login"])
api_router.include_router(
    users_router, prefix=settings.API_V1_STR + "/users", tags=["users"]
)
api_router.include_router(
    rooms_router, prefix=settings.API_V1_STR + "/rooms", tags=["rooms"]
)
