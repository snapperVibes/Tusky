__all__ = ["api_router"]
from datetime import timedelta
from uuid import UUID

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import settings, crud, schemas, models
from app.core import security
from app.routes._depends import login_required
from app.routes import _depends as deps

#######################################################################################
# login
login_router = APIRouter()


@login_router.get("/")
def home():
    return {"msg": "Welcome to Tusky's API 🐘."}


@login_router.post("/login/access-token", response_model=schemas.Token)
def login_access_token(
    db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    name, number = form_data.username.split("#")
    user = crud.user.authenticate(
        db, username=name, number=number, password=form_data.password
    )
    # Todo: There's no point to using this if you don't actually use it correctly
    user = user.ok()
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not crud.user.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


#######################################################################################
# rooms
rooms_router = APIRouter()


#######################################################################################
# users
users_router = APIRouter()


@users_router.post("/create", response_model=schemas.User)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_init: schemas.UserCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
):
    return crud.user.create(db, obj_init=user_init)


@users_router.get("/me", response_model=schemas.User)
def read_current_user(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    return current_user


#######################################################################################
# quiz
quiz_router = APIRouter()


# HUGE TODO: Although I'm 80% sure  get_current_active_user means that
#       login is required, it would be best to check.
@login_required
@quiz_router.post("/quizzes/create", response_model=schemas.Quiz)
def create_quiz(
    *,
    db: Session = Depends(deps.get_db),
    obj_init: schemas.QuizCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    return crud.quiz.create(db, obj_init=obj_init)


@quiz_router.get("/quizzes/get")
def get_quiz(*, db: Session = Depends(deps.get_db), owner: str, quiz_name: str):
    quiz_result = crud.quiz.get_by_owner_and_name(db, owner=owner, name=quiz_name)
    if quiz := quiz_result.ok():
        pass
    else:
        # Todo: Make this public facing
        raise quiz_result.err()
    if quiz.is_public:
        return quiz
    # Todo: Verification
    return quiz


@quiz_router.get("/answers/get_by_quiz")
def get_quiz(*, db: Session = Depends(deps.get_db), quiz_id: str):
    # Todo: Confirm quiz is public
    return crud.question.get_multi_by_quiz_id(db, quiz_id=quiz_id)


@login_required
@quiz_router.post("/questions/create")
def create_question(
    *,
    db: Session = Depends(deps.get_db),
    obj_init: schemas.QuestionCreate,
):
    crud.question.create(db, obj_init=obj_init)


#######################################################################################
api_router = APIRouter()
api_router.include_router(login_router, tags=["login"])
api_router.include_router(users_router, prefix="/users", tags=["users"])
api_router.include_router(rooms_router, prefix="/rooms", tags=["rooms"])
api_router.include_router(quiz_router, tags=["quizzes"])
