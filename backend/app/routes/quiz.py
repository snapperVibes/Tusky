from typing import List, Optional
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

# Todo: Assert permissions for posting quizzes on other people's accounts
@router.post("/create", response_model=schemas.Quiz)
def create_quiz(
    *,
    db: Session = Depends(deps.get_db),
    obj_in: schemas.QuizCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    if current_user.id != obj_in.owner_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You can only post quizzes to your own account.",
        )
    return crud.quiz.create(db, obj_in=obj_in)


@router.get("/getPreviewsByUser", response_model=List[schemas.Quiz])
def get_quiz_preview_by_user(
    *,
    db: Session = Depends(deps.get_db),
    owner_id: UUID,
):
    return crud.quiz.get_previews_by_user(db, owner_id=owner_id)


# Todo: Implement private quizzes
# @router.get("/getMyPreviews", response_model=List[schemas.Quiz])
# def get_my_quiz_previews(
#     *,
#     db: Session = Depends(deps.get_db),
#     current_user: models.User = Depends(deps.get_current_active_user),
# ):
#     return crud.quiz.get_previews_by_user(
#         db, owner_id=current_user.id, display_private=True


@router.get("/{id}", response_model=schemas.Quiz)
def get_quiz(*, db: Session = Depends(deps.get_db), id: UUID):
    # Todo: Confirm quiz is public
    return crud.quiz.get(db, id=id)


@router.patch("/update", response_model=schemas.Quiz)
def update_quiz(
    *,
    db: Session = Depends(deps.get_db),
    obj_in: schemas.QuizUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    quiz = crud.quiz.get(db=db, id=obj_in.id)
    if not quiz:
        raise Http404QuizNotFound
    if quiz.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You can only update quizzes that you own",
        )
    return crud.quiz.update(db=db, db_obj=quiz, obj_in=obj_in)


@router.delete("/{id}")
def delete_quiz(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    quiz = crud.quiz.get(db, id=id)
    if not quiz:
        raise Http404QuizNotFound
    if quiz.owner_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return {"removed": crud.quiz.remove(db, id=id)}


@router.post("/question/create", response_model=schemas.Question)
def create_question(
    *,
    db: Session = Depends(deps.get_db),
    obj_in: schemas.QuestionCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    # Todo: Separate method to get owner
    quiz_owner = crud.quiz.get(db, id=obj_in.quiz_id).owner_id
    if current_user.id != quiz_owner:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You can only post questions to your own quizzes",
        )
    return crud.question.create(db, obj_in=obj_in)


@router.patch("/question/update", response_model=schemas.Question)
def update_question(
    *,
    db: Session = Depends(deps.get_db),
    obj_in: schemas.QuestionUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    db_obj = crud.question.get(db, id=obj_in.id)
    quiz_owner = db_obj.quiz.owner_id
    if current_user.id != quiz_owner:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You can only modify questions belonging to your own quizzes.",
        )
    return crud.question.update(db, db_obj=db_obj, obj_in=obj_in)


@router.post("/answer/create", response_model=schemas.Answer)
def create_answer(
    *,
    db: Session = Depends(deps.get_db),
    obj_in: schemas.AnswerCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    # Todo: Separate method to get owner
    quiz_owner = crud.question.get(db, id=obj_in.question_id).quiz.owner_id
    if current_user.id != quiz_owner:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You can only post answers to your own quizzes",
        )
    return crud.question.create(db, obj_in=obj_in)


@router.patch("/answer/update", response_model=schemas.Answer)
def update_answer(
    *,
    db: Session = Depends(deps.get_db),
    obj_in: schemas.AnswerUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    db_obj = crud.answer.get(db, id=obj_in.id)
    quiz_owner = db_obj.question.quiz.owner_id
    if current_user.id != quiz_owner:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You can only modify answers belonging to your own quizzes.",
        )
    return crud.question.update(db, db_obj=db_obj, obj_in=obj_in)
