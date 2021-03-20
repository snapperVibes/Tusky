__all__ = ["user"]

from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from result import Ok, Err, Result
from sqlalchemy import desc
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Session

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
        obj_init: Union[UpdateSchemaType, Dict[str, Any]]
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
            name=obj_init.name,
            hashed_password=security.hash_password(obj_init.password),
            is_superuser=obj_init.is_superuser,
        )
        # Todo: This is a rough implementation. Adhere to best practices so we don't hit the db unnecessarily
        # Generate user number
        # Superusers can set their own number, normal users just get the next number
        if db_obj.is_superuser and (obj_init.number is not None):
            db_obj.number = obj_init.number
        else:
            q = (
                db.query(User.number)
                .filter_by(name=obj_init.name)
                .order_by(desc("number"))
                .first()
            )
            db_obj.number = int(q.number) + 1 if q is not None else 1
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_name_and_number(self, db: Session, *, name: str, number: int) -> Result[User, UserDoesNotExist]:
        user = db.query(User).filter(User.name == name, User.number == number).one_or_none()
        if user is None:
            return Err(UserDoesNotExist)
        return Ok(user)

    def authenticate(
        self, db: Session, *, username: str, number: int, password: str
    ) -> Result[User, Union[UserDoesNotExist, IncorrectPassword]]:
        # Todo: Make splitting name and number a method. Does it belong in schema?
        user_result = self.get_by_name_and_number(db, name=username, number=number)
        if user := user_result.ok():
            pass
        else:   # Propagate error
            return user_result.err()
        if not security.verify_password(password, user.hashed_password):
            return Err(IncorrectPassword(username, number))
        return Ok(user)

    # Todo: Figure out point of method. It's in the cookiecutter so there has to be a point, right?
    def is_active(self, user: User) -> bool:
        return user.is_active

    def is_superuser(selfself, user: User) -> bool:
        return user.is_superuser


user = CRUDUser(User)
