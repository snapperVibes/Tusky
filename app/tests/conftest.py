from typing import Generator, Dict

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import init_app, crud
from app.core import settings
from app.database import SessionLocal
from app.exceptions import UserDoesNotExist
from app.schemas import UserCreate
from app.tests.utils import random_string


@pytest.fixture(scope="session")
def db() -> Generator:
    yield SessionLocal()


@pytest.fixture(scope="module")
def client() -> Generator:
    app = init_app()
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="module")
def superuser_token_headers(client: TestClient) -> Dict[str, str]:
    login_data = {
        "username": settings.FIRST_SUPERUSER + "#0000",
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    res = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    tokens = res.json()
    access_token = tokens["access_token"]
    return {"Authorization": f"Bearer {access_token}"}


@pytest.fixture(scope="module")
def normal_user_token_headers(client: TestClient, db: Session) -> Dict[str, str]:
    name, number = settings.TEST_USER_NAME, 1
    user = crud.user.get_by_name_and_number(db, name=name, number=number)
    if user.ok():
        user = user.unwrap()
    elif user.err() == UserDoesNotExist:
        user_init_create = UserCreate(
            name=settings.TEST_USER_NAME,
            password=random_string()
        )
        user = crud.user.create(db, obj_init=user_init_create)
    return user_authentication_headers(
        client=client, name=user.name, number=user.number
    )
