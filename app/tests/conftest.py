import random
import string
from typing import Generator, Dict

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import init_app, crud, schemas
from app.core import settings
from app.database import SessionLocal


########################################################################################
# utils
def random_string() -> str:
    return "".join(random.choices(string.ascii_letters, k=32))


def get_user_authentication_headers(client, name_and_number, password):
    login_data = {"username": name_and_number, "password": password}
    res = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    tokens = res.json()
    access_token = tokens["access_token"]
    return {"Authorization": f"Bearer {access_token}"}


########################################################################################
# fixtures
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
    return get_user_authentication_headers(
        client=client,
        name_and_number=settings.FIRST_SUPERUSER + "#0001",
        password=settings.FIRST_SUPERUSER_PASSWORD,
    )


@pytest.fixture(scope="module")
def normal_user_token_headers(client: TestClient, db: Session) -> Dict[str, str]:
    """
    Returns a valid token for the test user.
    If the user doesn't exist, the user is first created.
    """
    password = random_string()
    user_init = schemas.UserCreate(
        display_name=settings.TEST_USER_NAME, password=password
    )
    user = crud.user.create(db, obj_init=user_init)
    return get_user_authentication_headers(
        client=client, name_and_number=user.name_and_number, password=password
    )
