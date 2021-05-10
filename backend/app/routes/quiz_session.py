from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import schemas, models, crud
from . import _depends as deps
from ..exceptions import Http404QuizNotFound

router = APIRouter(
    prefix="/sessions",
    tags=["sessions"],
)


@router.post("/create", response_model=schemas.QuizSession)
def create_session(
    *,
    db: Session = Depends(deps.get_db),
    obj_in: schemas.QuizSessionCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    room = crud.room.get(db, id=obj_in.room_id)
    if current_user.id != room.owner_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You can only create sessions in your own rooms.",
        )
    return crud.quiz_session.create(db, obj_in=obj_in)


@router.patch("/update", response_model=schemas.QuizSession)
def update_session(
    *,
    db: Session = Depends(deps.get_db),
    obj_in: schemas.QuizSessionUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    session = crud.quiz_session.get(db, id=obj_in.id)
    if current_user.id != session.room.owner_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You can only update sessions in your own rooms.",
        )
    return crud.quiz_session.update(db, db_obj=session, obj_in=obj_in)


@router.post("/response/create", response_model=schemas.StudentResponse)
def create_student_response(
    *,
    db: Session = Depends(deps.get_db),
    obj_in: schemas.StudentResponseCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    if current_user.id != obj_in.student_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You can only create responses for your own user.",
        )
    return crud.student_response.create(db, obj_in=obj_in)
