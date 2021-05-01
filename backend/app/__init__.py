__all__ = [
    # Functions
    "create_all",
    "drop_all",
]

from sqlalchemy.exc import InternalError, IntegrityError

from app.core import settings, security
from app import crud, schemas, main
from app.exceptions import Http404UserNotFound
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
        with db:
            owner = crud.user.create(db, obj_in=admin_obj)
            print("Admin created")
    except InternalError as err:
        with db:
            owner = crud.user.get_by_name(db, name="Admin#0000")
            if not owner:
                raise err
            print("Admin already exists")
            return

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
        name=QUIZ_NAME, owner_id=owner.id, questions=questions_inits
    )
    try:
        with db:
            crud.quiz.create(db, obj_in=quiz)
            print("Example quiz created")
    except IntegrityError:
        print("Example quiz already exists")


def drop_all(**kw):
    Base.metadata.drop_all(engine, **kw)
