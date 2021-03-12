from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Session

from app.core import security
from app.database import Base
from app.exceptions import Result, UserDoesNotExist, IncorrectPassword
from app.models import User
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
        return db.query(self.model).filter(self.model.id == id).first

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
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_name_and_number(self, db: Session, *, name: str, number: str):
        return db.query(User).filter(User.name == name, User.number == number)

    def authenticate(self, db: Session, *, username: str, number: str, password: str) -> Result[Optional[User], Optional[Union[UserDoesNotExist, IncorrectPassword]]]:
        err = None
        user = self.get_by_name_and_number(db, name=username, number=number)
        if not user:
            err = UserDoesNotExist(username, number)
            return Result(None, err)
        if not security.verify_password(password, user.hashed_password):
            err = IncorrectPassword(username, number)
            return Result(None, err)
        return Result(user, None)

    # Todo: Figure out point of method. It's in the cookiecutter so there has to be a point, right?
    def is_active(self, user: User) -> bool:
        return user.is_active

    def is_superuser(selfself, user: User) -> bool:
        return user.is_superuser

