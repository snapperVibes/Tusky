import random
import string


def random_string() -> str:
    return "".join(random.choices(string.ascii_letters, k=32))


# def user_authentication_headers(
#     *, client: TestClient, name: str, number: int, password: str
# ) -> Dict[str, str]:
#     data = {"username"}
