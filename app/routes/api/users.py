from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, schemas, models
from .. import depends as deps

router = APIRouter()


@router.post("/create", response_model=schemas.User)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_init: schemas.UserCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser)
):
    user = crud.user.create(db, obj_init=user_init)
    return user


@router.get("/me", response_model=schemas.User)
def read_current_user(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    return current_user
