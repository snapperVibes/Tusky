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
    admin_obj = schemas.UserCreate(
        display_name=settings.FIRST_SUPERUSER,
        password=settings.FIRST_SUPERUSER_PASSWORD,
        is_superuser=True,
    )
    try:
        crud.user.create(db, obj_init=admin_obj)
    except InternalError:
        pass
    # Add the example quiz
    QUIZ_NAME = "Example Quiz"
    questions_and_answers = [
        (
            "What is your name?",
            ["Sir Lancelot", "Sir Robin", "Sir Galahad", "King Arthur"],
        ),
        ("What is your quest?", ["To seek the Holy Grail"]),
        ("What is your favorite color?", ["Blue", "Yellow"]),
    ]
    questions_inits = []
    for question, answers in questions_and_answers:
        questions_inits.append(
            schemas.QuestionCreate(
                query=question, answers=[schemas.AnswerCreate(text=a) for a in answers]
            )
        )
    quiz = schemas.QuizCreate(
        name=QUIZ_NAME, owner="ADMIN#0000", questions=questions_inits
    )
    try:
        crud.quiz.create(db, obj_init=quiz)
    except PendingRollbackError:
        # Todo: Figure out more about this error and if there's a better error to catch
        #  Currently, this code only works on database initialization
        return
    print("YeeHaw 🐴")


def drop_all(**kw):
    Base.metadata.drop_all(engine, **kw)
