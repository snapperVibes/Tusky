from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import schemas, models, crud
from . import _depends as deps
from ..exceptions import Http404QuizNotFound

router = APIRouter(
    prefix="/quizzes",
    tags=["quizzes"],
)


@router.post("/create", response_model=schemas.Quiz)
def create_quiz(
    quiz: schemas.QuizCreate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    if current_user.id != quiz.owner_id:
        raise HTTPException(400, "You do not have permission to post this quiz.")
    return crud.quiz.create(db, obj_in=quiz)


@router.post("/get", response_model=schemas.Quiz)
def get_quiz(
    quiz_id: UUID,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    quiz_in_db = crud.quiz.get(db, quiz_id)
    if quiz_in_db.owner_id != current_user.id:
        raise HTTPException(400, "You do not have permission to get this quiz.")
    return quiz_in_db


@router.patch("/patch", response_model=schemas.Quiz)
def patch_quiz(
    quiz: schemas.QuizUpdate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """ Arguments: json-diff"""
    # Todo: Order errors for security
    quiz_in_db = crud.quiz.get(db, quiz.id)
    if current_user.id != quiz.id:
        raise HTTPException(400, "You do not have permission to get this quiz.")
    return crud.quiz.update(db, db_obj=quiz_in_db, obj_in=quiz)











