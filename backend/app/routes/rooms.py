from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas, models, crud
from . import _depends as deps
from ._depends import login_required

router = APIRouter(
    prefix="/rooms",
    tags=["rooms"],
)


@login_required
@router.post("/create", response_model=schemas.RoomPublic)
def create_room(
    *,
    db: Session = Depends(deps.get_db),
    obj_in: schemas.RoomCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    obj_in.owner_id = current_user.id
    return crud.room.create(db, obj_in=obj_in)


@router.get("/get-by-code", response_model=schemas.RoomPublic)
def get_room_by_code(
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
    code: str,
):
    return crud.room.get_by_code(db, code=code)


@router.put("/update", response_model=schemas.RoomPublic)
def update_room(
    *,
    db: Session = Depends(deps.get_db),
    obj_in: schemas.RoomUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    return crud.room.get(db, id=obj_in.id)
