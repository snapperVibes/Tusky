__all__ = ["user", "quiz", "room"]

# Todo: These methods fetch unnecessary information by default
#  If efficiency becomes an issue,
#  API Endpoints should get their own custom CRUD methods

from typing import (
    Any,
    Dict,
    Generic,
    List,
    Optional,
    Type,
    TypeVar,
    Union,
    NamedTuple,
)

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
from sqlalchemy.util import symbol

from app.core import security
from app.exceptions import (
    Http404UserNotFound,
    Http400IncorrectPassword,
    Http404ActiveRoomNotFound,
    Http404InvalidRequestError,
    Http404QuizNotFound,
    IntegrityError, Http403QuizNameConflict,
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
    QuestionUpdate,
    AnswerCreate,
    AnswerUpdate,
)

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class _ModelAndSchema(NamedTuple):
    model: Optional[ModelType]
    schema: Optional[Union[CreateSchemaType, UpdateSchemaType, Dict]]


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
        print("obj_data type", type(obj_data))
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:

            if field in update_data:
                print(update_data[field])
                setattr(db_obj, field, update_data[field])

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: UUID) -> int:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return 1

    # # Todo: Typing: I don't understand what a symbol is,
    # #  and Pycharm says it's the wrong type
    # def _match_by_id(
    #     self, db_objs: symbol, objs_in: Optional[List[Union[UpdateSchemaType, Dict]]]
    # ) -> Dict[UUID, _ModelAndSchema]:
    #     # Helper function for updating nested models.
    #     id_to_db_obj = {obj.id: obj for obj in db_objs}
    #     id_to_obj_in = {obj.id: obj for obj in objs_in}
    #     result = {}
    #     for id in id_to_db_obj.keys() | id_to_obj_in.keys():
    #         result[id] = _ModelAndSchema(
    #             model=id_to_db_obj.get(id, None),
    #             schema=id_to_obj_in.get(id, None),
    #         )
    #     return result


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
        if obj_in.is_superuser and not (identifier_name == "admin"):
            raise PermissionError("Only admins can create super users")
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
                raise ValueError("A number and hash symbol were both passed")
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


class CRUDAnswer(_CRUDBase[Answer, AnswerCreate, AnswerUpdate]):
    def remove(self, db: Session, *, id: UUID) -> int:
        db.execute(
            text("SELECT delete_single_answer(:id)").bindparams(id=id),
        )
        db.commit()
        return 1


_delete_single_answer = DDL(
    """\
CREATE FUNCTION delete_single_answer(answer_id UUID) RETURNS INT AS $$
    '''
    Changes the previous answer of the next answer if the current answer is deleted.

    Example Answer table:
        id | previous_answer
        ---|---
        1  | null
        2  | 1
        3  | 2

        If answer with id 2 is deleted,
        this function changes answer 3 so the table looks like this:
        id | previous_answer
        ---|---
        1  | null
        3  | 1
    '''
    # Todo: Optimize
    select_plan = plpy.prepare(
        "SELECT previous_answer FROM answer WHERE id = $1", ["UUID"]
    )
    rows = plpy.execute(select_plan, [answer_id])
    if len(rows) > 1:
        raise plpy.Error(
        "Tusky failed a sanity check: "
        "multiple answers pointed towards the same previous_answer.",
    )
    previous_id = rows[0]["previous_answer"]
    update_plan = plpy.prepare(
        "UPDATE answer SET previous_answer = $1 WHERE previous_answer = $2;",
        ["UUID", "UUID"]
    )
    plpy.execute(
        update_plan,
        [previous_id, answer_id]
    )
    delete_plan = plpy.prepare("DELETE FROM answer WHERE id = $1", ["UUID"])
    plpy.execute(
        delete_plan,
        [answer_id]
    )
    return 1
$$ LANGUAGE PLPYTHON3U;"""
)
event.listen(
    Answer.__table__, "after_create", _delete_single_answer.execute_if(dialect="postgresql")
)


class CRUDQuestion(_CRUDBase[Question, QuestionCreate, QuestionUpdate]):
    pass


class CRUDQuiz(_CRUDBase[Quiz, QuizCreate, QuizUpdate]):
    def create(self, db: Session, *, obj_in: QuizCreate) -> Quiz:
        try:
            quiz = super(CRUDQuiz, self).create(db, obj_in=obj_in)
        except sqlalchemy_IntegrityError as err:
            raise Http403QuizNameConflict from err
        return quiz

    def update(
        self,
        db: Session,
        *,
        db_obj: Quiz,
        obj_in: Union[QuizUpdate, Dict[str, Any]],
    ) -> Quiz:
        try:
            quiz = super(CRUDQuiz, self).update(db, db_obj=db_obj, obj_in=obj_in)
        except sqlalchemy_IntegrityError as err:
            raise Http403QuizNameConflict from  err
        return quiz

    def get_previews_by_user(
        self,
        db: Session,
        *,
        owner_id: UUID,
    ) -> Quiz:
        # Todo: Pagination
        # Todo: Don't fetch unnecessary information
        try:
            quiz = db.query(self.model).filter(User.id == owner_id).all()
        except (sqlalchemy_MultipleResultsFound) as err:
            raise Http404InvalidRequestError from err
        if quiz is None:
            raise Http404QuizNotFound
        return quiz


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
                raise Http404ActiveRoomNotFound from err
            raise Http404InvalidRequestError from err


user = CRUDUser(User)
answer = CRUDAnswer(Answer)
question = CRUDQuestion(Question)
quiz = CRUDQuiz(Quiz)
room = CRUDRoom(Room)
