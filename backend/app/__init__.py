__all__ = [
    # Functions
    "create_all",
    "drop_all",
]

from sqlalchemy.exc import InternalError, IntegrityError

from app.core import settings, security
from app import crud, schemas, main
from app.exceptions import Http404UserNotFound
from app.models import Base, set_event_listeners
from app.database import engine, SessionLocal


def create_all(**kw):
    set_event_listeners()
    Base.metadata.create_all(engine, **kw)
    db = SessionLocal()

    # Add the super user
    admin_in = schemas.UserCreate(
        display_name=settings.FIRST_SUPERUSER,
        password=settings.FIRST_SUPERUSER_PASSWORD,
        is_superuser=True,
    )
    try:
        with db:
            admin = crud.user.create(db, obj_in=admin_in)
            print("Admin created")
    except InternalError as err:
        with db:
            admin = crud.user.get_by_name(db, name="Admin#0000")
            if not admin:
                raise err
            print("Admin already exists")
            return

    quiz_in = schemas.QuizCreate(title="Example Quiz", owner_id=admin.id)
    questions_and_answers = [
        (
            "What is your name?",
            ["Sir Lancelot", "Sir Robin", "Sir Galahad", "King Arthur"],
        ),
        ("What is your quest?", ["To seek the Holy Grail"]),
        ("What is your favorite color?", ["Blue", "Yellow"]),
    ]
    with db:
        quiz = crud.quiz.create(db, obj_in=quiz_in)
        previous_question_id = None
        for q, answers in questions_and_answers:
            question_in = schemas.QuestionCreate(
                query=q, quiz_id=quiz.id, previous_question=previous_question_id
            )
            question = crud.question.create(db, obj_in=question_in)
            previous_question_id = question.id
            previous_answer_id = None
            for j, a in enumerate(answers):
                answer_in = schemas.AnswerCreate(
                    text=a,
                    question_id=previous_question_id,
                    previous_answer=previous_answer_id,
                    is_correct=True if j == 0 else False,
                )
                answer = crud.answer.create(db, obj_in=answer_in)
                previous_answer_id = answer.id
    print("Example quiz created")


def drop_all(**kw):
    Base.metadata.drop_all(engine, **kw)
