from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import deps, schemas, crud
from app.external import Snowflake

router = APIRouter()


@router.post("/quiz", response_model=schemas.QuizResponse)
async def create_quiz(
    *,
    db: Session = Depends(deps.get_db),
    user=Depends(deps.get_current_active_user),
    obj_in: schemas.QuizCreate,
):
    quiz = await crud.quiz.create(db, obj_in=obj_in)
    return quiz


@router.patch("/quiz/{quiz_id}", response_model=schemas.QuizResponse)
def patch_quiz(
    *,
    db: Session = Depends(deps.get_db),
    user=Depends(deps.get_current_active_user),
    quiz_id: Snowflake,
    patch: schemas.QuizPatch,
):
    quiz = crud.quiz.get(db, id=quiz_id)
    print(quiz)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    quiz = crud.quiz.patch(db, db_obj=quiz, patch=patch)
    return quiz
