from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import schemas, models, crud
from . import _depends as deps
from ._depends import login_required
from ..exceptions import Http404QuizNotFound

router = APIRouter(
    prefix="/quizzes",
    tags=["quizzes"],
)


# Todo: Assert permissions for posting quizzes on other people's accounts
@login_required
@router.post("/create", response_model=schemas.QuizPublic)
def create_quiz(
    *,
    db: Session = Depends(deps.get_db),
    obj_in: schemas.QuizCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    if current_user.id != obj_in.owner:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only post quizzes to your own account",
        )
    return crud.quiz.create(db, obj_in=obj_in)


@router.get("/getPreview", response_model=schemas.QuizPreview)
def get_quiz_preview(
    *, db: Session = Depends(deps.get_db), quiz_name: str, owner_id: UUID
):
    """ Raises: Http404InvalidRequestError, Http404QuizNotFound"""
    return crud.quiz.get_previews(db, owner_id=owner_id, quiz_name=quiz_name)


@router.get("/getPreviewsByUser", response_model=List[schemas.QuizPublic])
def get_quiz_preview_by_user(
    *,
    db: Session = Depends(deps.get_db),
    owner_id: UUID,
):
    return crud.quiz.get_previews_by_user(db, owner_id=owner_id)


# Todo: Implement private quizzes
# @router.get("/getMyPreviews", response_model=List[schemas.QuizPublic])
# def get_my_quiz_previews(
#     *,
#     db: Session = Depends(deps.get_db),
#     current_user: models.User = Depends(deps.get_current_active_user),
# ):
#     return crud.quiz.get_previews_by_user(
#         db, owner_id=current_user.id, display_private=True


@router.get("/get", response_model=schemas.QuizPublic)
def get_quiz(
    *, db: Session = Depends(deps.get_db), id: UUID
):
    # Todo: Confirm quiz is public
    return crud.quiz.get(db, id=id)


@router.put(
    "/update",
    response_model=schemas.QuizPublic,
)
def update_quiz(
    *,
    db: Session = Depends(deps.get_db),
    obj_in: schemas.QuizUpdate,
):
    quiz = crud.quiz.get(db=db, id=obj_in.id)
    # Todo: Add measures to allow a quiz to safely switch owners
    # if quiz_in.owner != quiz.owner_id:
    #     raise ValueError("The owner of the quiz does not match the owner provided")
    if not quiz:
        raise Http404QuizNotFound
    return crud.quiz.update(db=db, db_obj=quiz, obj_in=obj_in)
