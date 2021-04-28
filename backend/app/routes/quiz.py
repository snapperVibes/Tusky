from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas, models, crud
from . import _depends as deps
from ._depends import login_required


router = APIRouter(
    prefix="/quizzes",
    tags=["quizzes"],
)


# HUGE TODO: Although I'm 80% sure  get_current_active_user means that
#       login is required, it would be best to check.
@login_required
@router.post("/create", response_model=schemas.QuizPublic)
def create_quiz(
    *,
    db: Session = Depends(deps.get_db),
    obj_in: schemas.QuizCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    return crud.quiz.create(db, obj_in=obj_in)


@router.get("/getTitle")
def get_quiz_title(
    *, db: Session = Depends(deps.get_db), quiz_name: str, owner_id: UUID
):
    quiz_result = crud.quiz.get_basics(db, quiz_name=quiz_name, owner_id=owner_id)
    if quiz := quiz_result.ok():
        pass
    else:
        # Todo: Make this public facing
        raise quiz_result.err()
    if quiz.is_public:
        return quiz
    # Todo: Verification
    return quiz


@router.get("/get", response_model=schemas.QuizPublic)
def get_full_quiz(
    *, db: Session = Depends(deps.get_db), quiz_name: str, owner_id: UUID
):
    # Todo: Figure out depends so we can have owner / name be a schema
    # Todo: Confirm quiz is public
    return crud.quiz.get_full(db, quiz_name=quiz_name, owner_id=owner_id)


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
        raise HTTPException(status_code=404, detail="Item not found")
    # if not crud.user.is_superuser(current_user) and (item.owner_id != current_user.id):
    #     raise HTTPException(status_code=400, detail="Not enough permissions")
    quiz = crud.quiz.update(db=db, db_obj=quiz, obj_in=obj_in)
    return quiz
