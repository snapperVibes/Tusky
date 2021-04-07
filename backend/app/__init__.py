__all__ = [
    # Functions
    "create_all",
    "drop_all",
]

from sqlalchemy.exc import InternalError, PendingRollbackError

from app.core import settings, security
from app import crud, schemas, main
from app.models import Base
from app.database import engine, SessionLocal


def create_all(**kw):
    # Create the tables
    Base.metadata.create_all(engine, **kw)
    db = SessionLocal()

    # Add the super user
    super_user = schemas.UserCreate(
        display_name=settings.FIRST_SUPERUSER,
        password=settings.FIRST_SUPERUSER_PASSWORD,
        is_superuser=True,
    )
    try:
        crud.user.create(db, obj_init=super_user)
    except InternalError:
        pass

    # Add the example quiz
    QUIZ_NAME = "Example Quiz"
    OWNER_NAME = "ADMIN#0000"
    quiz = schemas.QuizCreate(name=QUIZ_NAME, owner=OWNER_NAME)
    try:
        crud.quiz.create(db, obj_init=quiz)
    except PendingRollbackError:
        # Todo: Figure out more about this error and if there's a better error to catch
        return
    # Add questions to quiz
    queries = [
        "What is your name?",
        "What is your quest?",
        "What is your favorite color?",
    ]
    for query in queries:
       q = schemas.QuestionCreate(
            query=query, quiz_name=QUIZ_NAME, owner_name=OWNER_NAME
       )
       crud.question.create(db, obj_init=q)
    print("YeeHaw 🐴")


def drop_all(**kw):
    Base.metadata.drop_all(engine, **kw)