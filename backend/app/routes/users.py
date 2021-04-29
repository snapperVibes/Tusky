from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import schemas, models, crud
from . import _depends as deps

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post("/create", response_model=schemas.UserPublic)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserCreate,
):
    return crud.user.create(db, obj_in=user_in)


@router.get("/get-by-name", response_model=schemas.UserPublic)
def get_user_by_name(*, db: Session = Depends(deps.get_db), name: str, number: int):
    user_result = crud.user.get_by_name(db=db, name=name, number=number)
    if user := user_result.ok():
        return user
    raise user.err()


@router.get("/me", response_model=schemas.UserPublic)
def read_current_user(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    return current_user