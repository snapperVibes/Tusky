__all__ = ["user"]

from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from result import Ok, Err, Result
from sqlalchemy import desc, DDL, event
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from tenacity import retry, stop_after_attempt

from app import models
from app.core import security
from app.exceptions import UserDoesNotExist, IncorrectPassword
from app.models import Base, User
from app.schemas import UserCreate, UserUpdate

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class _CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def create(self, db: Session, *, obj_init: CreateSchemaType) -> ModelType:
        obj_init_data = jsonable_encoder(obj_init)
        db_obj = self.model(**obj_init_data)  # type: ignore
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
        obj_init: Union[UpdateSchemaType, Dict[str, Any]],
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_init, dict):
            update_data = obj_init
        else:
            update_data = obj_init.dict(exclude_unset=True)
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
    def create(self, db: Session, *, obj_init: UserCreate) -> User:
        db_obj = User(
            display_name=obj_init.display_name,
            hashed_password=security.hash_password(obj_init.password),
            is_superuser=obj_init.is_superuser,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_name_and_number(
        self, db: Session, *, name: str, number: int
    ) -> Result[User, UserDoesNotExist]:
        normalized_name = security.to_identifier(name)
        _user = (
            db.query(User)
            .filter(User.identifier_name == normalized_name, User.number == number)
            .one_or_none()
        )
        if _user is None:
            return Err(UserDoesNotExist)
        return Ok(_user)

    def authenticate(
        self, db: Session, *, username: str, number: int, password: str
    ) -> Result[User, Union[UserDoesNotExist, IncorrectPassword]]:
        user_result = self.get_by_name_and_number(db, name=username, number=number)
        if user := user_result.ok():
            pass
        else:  # Propagate error
            return user_result.err()
        if not security.verify_password(password, user.hashed_password):
            return Err(IncorrectPassword(username, number))
        return Ok(user)

    # Todo: Figure out point of method. It's in the cookiecutter so there has to be a point, right?
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
    if id_name == "admin":
        count_row = plpy.execute("SELECT count(display_name) FROM public.user WHERE display_name='admin';")
        if count_row[0]['count'] > 0:
            raise ValueError("Name cannot be admin.")
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

_set_number_func = DDL(
    """\
CREATE OR REPLACE FUNCTION _set_number_func() RETURNS TRIGGER AS $$
    row = plpy.execute("SELECT number FROM public.user ORDER BY number DESC LIMIT 1;")
    try:
       TD["new"]["number"] = row[0]["number"] + 1
    except IndexError:
       TD["new"]["number"] = 1
    return "MODIFY"
$$ LANGUAGE PLPYTHON3U;"""
)
_set_number_trigger = DDL(
    """\
CREATE TRIGGER _set_number_trigger BEFORE INSERT on public.user
FOR EACH ROW EXECUTE PROCEDURE _set_number_func();"""
)
event.listen(
    User.__table__, "after_create", _set_number_func.execute_if(dialect="postgresql")
)
event.listen(
    User.__table__, "after_create", _set_number_trigger.execute_if(dialect="postgresql")
)
