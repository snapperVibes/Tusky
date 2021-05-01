__all__ = ["user", "quiz", "room"]

from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import DDL, event, desc, text, bindparam, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.engine import CursorResult
from sqlalchemy.exc import (
    NoResultFound as sqlalchemy_NoResultFound,
    MultipleResultsFound as sqlalchemy_MultipleResultsFound,
    IntegrityError as sqlalchemy_IntegrityError,
)
from sqlalchemy.orm import Session

from app.core import security
from app.exceptions import (
    Http404UserNotFound,
    Http400IncorrectPassword,
    Http404ActiveRoomNotFound,
    Http404InvalidRequestError,
    Http404QuizNotFound,
    IntegrityError,
)
from app.models import Base, User, Quiz, Question, Answer, Room
from app.schemas import (
    UserCreate,
    UserUpdate,
    QuizCreate,
    QuizUpdate,
    RoomCreate,
    RoomUpdate,
    QuestionCreate,
)

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


# Todo: Wrap defaults in Results
class _CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)  # Todo: Look up what this does
        return db_obj

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]],
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: UUID) -> ModelType:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj


class CRUDUser(_CRUDBase[User, UserCreate, UserUpdate]):
    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        # The purpose of using SQLAlchemy is to make life easier
        #  Sometimes, writing raw SQL is easiest way to express your thoughts
        statement = text(
            """
            WITH highest_number AS (
              SELECT COALESCE(
                (
                  SELECT number FROM "user"
                    WHERE identifier_name = :identifier_name
                    ORDER BY number desc limit 1
                ),
                0
              )
            )
            INSERT INTO "user"(
              display_name, hashed_password, is_superuser, is_active,
              number
            )
            VALUES(
              :display_name, :hashed_password, :is_superuser, true,
              (SELECT * FROM highest_number) + 1
            )
            RETURNING *
            """
        )
        identifier_name = security.to_identifier(obj_in.display_name)
        hashed_password = security.hash_password(obj_in.password)
        cursor: CursorResult = db.execute(
            statement,
            {
                "display_name": obj_in.display_name,
                "hashed_password": hashed_password,
                "is_superuser": obj_in.is_superuser,
                "identifier_name": identifier_name,
            },
        )
        db.commit()
        row = cursor.mappings().one()
        return User(**row)

    def get_by_name(
        self, db: Session, *, name: str, number: Optional[int] = None
    ) -> User:
        """ Raises: Http404UserNotFound """
        # Allows a name to be passed as
        # name='exampleuser#1234' or name='exampleuser', number=1234
        _name, _, _number = name.partition("#")
        if _number:
            if number:
                raise ("A number and hash symbol were both passed")
            number = _number

        if not (_name and number):
            # Todo: Error handling
            pass

        normalized_name = security.to_identifier(_name)
        # Todo: normalize errors. Maybe use "one" instead of "one or none"?
        _user = (
            db.query(User)
            .filter(User.identifier_name == normalized_name, User.number == number)
            .one_or_none()
        )
        if _user is None:
            raise Http404UserNotFound
        return _user

    def authenticate(self, db: Session, *, username: str, password: str) -> User:
        """Raises: Http404UserNotFound, Http400IncorrectPassword"""
        user = self.get_by_name(db, name=username)
        if not security.verify_password(password, user.hashed_password):
            raise Http400IncorrectPassword
        return user

    # Todo: Figure out point of method. It's in the cookiecutter so there has to be a
    #  point, right?
    def is_active(self, user: User) -> bool:
        return user.is_active

    def is_superuser(self, user: User) -> bool:
        return user.is_superuser


user = CRUDUser(User)

# Database functions don't seem Pythonic.
# I wish I could talk to industry people and learn best practices
_to_identifier_func = DDL(
    """\
CREATE FUNCTION _to_identifier_func() RETURNS TRIGGER AS $$
    import unicodedata
    disp_name = TD["new"]["display_name"]
    id_name = unicodedata.normalize("NFKD", disp_name).lower()
    TD["new"]["identifier_name"] = id_name
    if id_name.__contains__("admin"):
        count_row = plpy.execute("SELECT count(display_name) FROM public.user WHERE display_name='admin';")
        if count_row[0]['count'] > 0:
            raise ValueError("Name cannot be admin.")
        TD["new"]["number"] = 0
    if id_name.__contains__("#"):
        raise ValueError("The normalized name cannot contain the hash symbol")
    if len(id_name) > 32:
        raise ValueError("The normalized name cannot be longer than 32 characters")
    return "MODIFY"
$$ LANGUAGE PLPYTHON3U;"""
)
_to_identifier_trigger = DDL(
    """\
CREATE TRIGGER _to_identifier_trigger BEFORE INSERT OR UPDATE on public.user
FOR EACH ROW EXECUTE PROCEDURE _to_identifier_func();"""
)
event.listen(
    User.__table__, "after_create", _to_identifier_func.execute_if(dialect="postgresql")
)
event.listen(
    User.__table__,
    "after_create",
    _to_identifier_trigger.execute_if(dialect="postgresql"),
)


class CRUDQuiz(_CRUDBase[Quiz, QuizCreate, QuizUpdate]):
    def create(self, db: Session, *, obj_in: QuizCreate) -> Quiz:
        # Todo: Learn SQLAlchemy relations; it handles getting foreign keys for us
        db_quiz_obj = Quiz(name=obj_in.name, owner_id=obj_in.owner)
        db.add(db_quiz_obj)
        try:
            db.flush()
        except sqlalchemy_IntegrityError as err:
            raise IntegrityError(
                status_code=400,
                detail="Two quizzes by the same owner cannot have the same name.",
            ) from err
        db.refresh(db_quiz_obj)
        # Add questions and answers
        self._create_questions_and_answers(db, obj_in=obj_in, db_quiz_obj=db_quiz_obj)
        db.commit()
        db.refresh(db_quiz_obj)
        return db_quiz_obj

    def _create_questions_and_answers(
        self, db: Session, *, obj_in: QuizCreate, db_quiz_obj: Quiz
    ):
        if not db_quiz_obj.questions:
            return
        for _question in obj_in.questions:
            db_question_obj = Question(quiz_id=db_quiz_obj.id, query=_question.query)
            db.add(db_question_obj)
            db.flush()
            db.refresh(db_question_obj)
            self._create_answers(
                db,
                obj_in=_question,
                db_question_obj=db_question_obj,
                previous_answer_id=None,
            )

    def _create_answers(
        self,
        db,
        *,
        obj_in: QuestionCreate,
        db_question_obj: Question,
        previous_answer_id: Optional[UUID],
    ):
        if not obj_in.answers:
            return
        for _answer in obj_in.answers:
            db_answer_obj = Answer(
                question_id=db_question_obj.id,
                text=_answer.text,
                previous_answer=previous_answer_id,
            )
            db.add(db_answer_obj)
            db.flush()
            db.refresh(db_answer_obj)
            previous_answer_id = db_answer_obj.id

    def get_previews(self, db: Session, *, owner_id: UUID, quiz_name: str) -> Quiz:
        """ Raises: Http404InvalidRequestError, Http404QuizNotFound"""
        try:
            quiz = (
                db.query(self.model)
                .filter(User.id == owner_id, Quiz.name == quiz_name)
                .one_or_none()
            )
        except (sqlalchemy_MultipleResultsFound) as err:
            raise Http404InvalidRequestError from err
        if quiz is None:
            raise Http404QuizNotFound
        return quiz

    def get_previews_by_user(
        self,
        db: Session,
        *,
        owner_id: UUID,
    ) -> Quiz:
        # Todo: Pagination
        try:
            quiz = db.query(self.model).filter(User.id == owner_id).all()
        except (sqlalchemy_MultipleResultsFound) as err:
            raise Http404InvalidRequestError from err
        if quiz is None:
            raise Http404QuizNotFound
        return quiz

    def get_full(self, db: Session, *, quiz_name: str, owner_id: UUID) -> Quiz:
        """ Raises: Http404InvalidRequestError, Http404QuizNotFound"""

        quiz_ = self.get_previews(db, owner_id=owner_id, quiz_name=quiz_name)
        questions = db.query(Question).filter(Question.quiz_id == quiz_.id).all()
        for q in questions:
            q.answers = db.query(Answer).filter(Answer.question_id == q.id).all()
        quiz_.questions = questions
        return quiz_


quiz = CRUDQuiz(Quiz)


class CRUDRoom(_CRUDBase[Room, RoomCreate, RoomUpdate]):
    def get_by_code(self, db: Session, *, code: str) -> Room:
        """ Raises: sqlalchemy_NoResultFound, sqlalchemy_MultipleResultsFound"""
        try:
            return (
                db.query(Room).filter(Room.code == code, Room.is_active == True).one()
            )
        except (
            sqlalchemy_NoResultFound,
            sqlalchemy_MultipleResultsFound,
        ) as err:
            # I am excited for pattern matching in Python 3.10!
            if type(err) == sqlalchemy_NoResultFound:
                raise Http404ActiveRoomNotFound(from_=err)
            raise Http404InvalidRequestError(from_=err)


room = CRUDRoom(Room)
