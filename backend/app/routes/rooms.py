from fastapi import APIRouter, Depends
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
def get_room_by_code(*, db: Session = Depends(deps.get_db), code: str):
    room_result = crud.room.get_by_code(db, code=code)
    if room := room_result.ok():
        pass
    else:
        raise room_result.err()
    return room


@router.put("/update", response_model=schemas.RoomPublic)
def update_room(*, db: Session = Depends(deps.get_db), obj_in: schemas.RoomUpdate):
    return crud.room.get(db, id=obj_in.id)
