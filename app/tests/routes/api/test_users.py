from typing import Dict

from fastapi.testclient import TestClient

from app import crud
from app.core import settings
from app.tests.utils import random_string


def test_get_users_superuser_me(
    client: TestClient, superuser_token_headers: Dict[str, str]
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=superuser_token_headers)
    current_user = r.json()
    print(current_user)
    assert current_user
    assert current_user["is_active"] is True
    assert current_user["is_superuser"]
    assert current_user["name"] == settings.FIRST_SUPERUSER


# def test_get_users_normal_user_me(
#     client: TestClient, normal_user_token_headers: Dict[str, str]
# ) -> None:
#     r = client.get(f"{settings.API_V1_STR}/users/me", headers=normal_user_token_headers)
#     current_user = r.json()
#     assert current_user
#     assert current_user["is_active"] is True
#     assert current_user["is_superuser"] is False
#     assert current_user["email"] == settings.EMAIL_TEST_USER
