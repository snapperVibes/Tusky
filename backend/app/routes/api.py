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
from app.schemas import QuizGet, QuizUpdate

login_router = APIRouter()


@login_router.get("/")
def home():
    return {"msg": "Welcome to Tusky's API 🐘."}


@login_router.post("/login/access-token", response_model=schemas.Token)
def login_access_token(
    db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm),
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


@users_router.post("/create", response_model=schemas.UserPublic)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_init: schemas.UserCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
):
    return crud.user.create(db, obj_init=user_init)


@users_router.get("/get-by-name", response_model=schemas.UserPublic)
def get_by_name(*, db: Session = Depends(deps.get_db), name: str, number: int):
    user_result = crud.user.get_by_name(db=db, name=name, number=number)
    if user := user_result.ok():
        return user
    raise user.err()


@users_router.get("/me", response_model=schemas.UserPublic)
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
@quiz_router.post("/create", response_model=schemas.QuizPublic)
def create_quiz(
    *,
    db: Session = Depends(deps.get_db),
    obj_init: schemas.QuizCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    return crud.quiz.create(db, obj_init=obj_init)


@quiz_router.get("/getTitle")
def get_quiz_title(
    *, db: Session = Depends(deps.get_db), quiz_get: QuizGet = Depends(QuizGet)
):
    quiz_result = crud.quiz.get_basics(db, obj_init=quiz_get)
    if quiz := quiz_result.ok():
        pass
    else:
        # Todo: Make this public facing
        raise quiz_result.err()
    if quiz.is_public:
        return quiz
    # Todo: Verification
    return quiz


@quiz_router.get("/get", response_model=schemas.QuizPublic)
def get_full_quiz(
    *, db: Session = Depends(deps.get_db), quiz_get: QuizGet = Depends(QuizGet)
):
    # Todo: Figure out depends so we can have owner / name be a schema
    # Todo: Confirm quiz is public
    return crud.quiz.get_full(db, obj_init=quiz_get)


@quiz_router.put("/update", response_model=schemas.QuizPublic)
def update_quiz(
    *,
    db: Session = Depends(deps.get_db),
    quiz_init: schemas.QuizUpdate,
):
    quiz = crud.quiz.get(db=db, id=quiz_init.id)
    # Todo: Add measures to allow a quiz to safely switch owners
    if quiz_init.owner != quiz.owner_id:
        raise ValueError("The owner of the quiz does not match the owner provided")
    if not quiz:
        raise HTTPException(status_code=404, detail="Item not found")
    # if not crud.user.is_superuser(current_user) and (item.owner_id != current_user.id):
    #     raise HTTPException(status_code=400, detail="Not enough permissions")
    quiz = crud.quiz.update(db=db, db_obj=quiz, obj_init=quiz_init)
    return quiz


#######################################################################################
api_router = APIRouter()
api_router.include_router(login_router, tags=["login"])
api_router.include_router(users_router, prefix="/users", tags=["users"])
api_router.include_router(rooms_router, prefix="/rooms", tags=["rooms"])
api_router.include_router(quiz_router, prefix="/quizzes", tags=["quizzes"])
