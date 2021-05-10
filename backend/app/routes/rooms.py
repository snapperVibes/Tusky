from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas, models, crud
from . import _depends as deps

router = APIRouter(
    prefix="/rooms",
    tags=["rooms"],
)


@router.post("/create", response_model=schemas.Room)
def create_room(
    *,
    db: Session = Depends(deps.get_db),
    obj_in: schemas.RoomCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    obj_in.owner_id = current_user.id
    room = crud.room.create(db, obj_in=obj_in)
    return room


@router.get("/get-by-code", response_model=schemas.Room)
def get_room_by_code(
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
    code: str,
):
    room = crud.room.get_by_code(db, code=code)
    room.session
    print("\n"*3, room.__dict__)
    return room


@router.put("/update", response_model=schemas.Room)
def update_room(
    *,
    db: Session = Depends(deps.get_db),
    obj_in: schemas.RoomUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    return crud.room.get(db, id=obj_in.id)
