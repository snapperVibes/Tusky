from functools import partial
from typing import Dict

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import schemas

from app.core import settings


def test_get_users_superuser_me(
    client: TestClient, superuser_token_headers: Dict[str, str]
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=superuser_token_headers)
    current_user = r.json()
    print(current_user)
    assert current_user
    assert current_user["is_active"] is True
    assert current_user["is_superuser"]
    assert current_user["display_name"] == settings.FIRST_SUPERUSER
    assert current_user["number"] == "0000"


def test_get_users_normal_user_me(
    client: TestClient, normal_user_token_headers: Dict[str, str]
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=normal_user_token_headers)
    current_user = r.json()
    assert current_user
    assert current_user["is_active"] is True
    assert current_user["is_superuser"] is False
    assert current_user["display_name"] == settings.TEST_USER_NAME


def test_unique_numbers(client: TestClient, superuser_token_headers: dict, db: Session):
    # Todo: This currently fails because of an oversight considering letter case. Fix it.
    _post = partial(
        client.post,
        f"{settings.API_V1_STR}/users/create",
        headers=superuser_token_headers,
    )
    user1_init = schemas.UserCreate(display_name="dave", password="insecurE&123")
    user2_init = schemas.UserCreate(display_name="dave", password="insecurE&123")
    user3_init = schemas.UserCreate(display_name="dave", password="differeNt&456")
    user4_init = schemas.UserCreate(display_name="Dave", password="insecurE&123")
    user5_init = schemas.UserCreate(display_name="Dave", password="differeNt&456")
    r1 = _post(json=user1_init.dict())
    r2 = _post(json=user2_init.dict())
    r3 = _post(json=user3_init.dict())
    r4 = _post(json=user4_init.dict())
    r5 = _post(json=user5_init.dict())
    u1 = r1.json()
    u2 = r2.json()
    u3 = r3.json()
    u4 = r4.json()
    u5 = r5.json()
    print(u1)
    assert u1["display_name"] == u2["display_name"] == u3["display_name"] == "dave"
    assert u4["display_name"] == u5["display_name"] == "Dave"
    users = [u1, u2, u3, u4, u5]
    assert len(set(u["number"] for u in users)) == len(users)
    assert [u["identifier_name"] == "dave" for u in users]
