import random

import pytest
from fastapi.testclient import TestClient

from .__init__ import Discriminator, app


@pytest.fixture
def STOP_AT_100():
    return [50, 98, 54, 6, 34, 66, 63, 52, 39, 62, 46, 75, 28, 65, 18, 37, 85, 13, 80, 33, 69, 78, 19, 40, 82, 10, 43, 61, 88, 89, 56, 41, 27, 90, 57, 95, 4, 92, 59, 36, 72, 1, 96, 47, 97, 26, 70, 51, 73, 68, 58, 76, 32, 22, 16, 21, 5, 71, 84, 15, 45, 74, 35, 29, 86, 99, 44, 79, 93, 38, 83, 30, 23, 31, 60, 11, 25, 7, 20, 67, 77, 87, 48, 3, 81, 42, 53, 64, 17, 55, 94, 91, 2, 14, 49, 8, 12, 9, 24]  # fmt: skip


@pytest.fixture
def ordered_discriminator():
    return Discriminator(seed=9260, position=0, start=1, stop=8)


def test_meta(STOP_AT_100, ordered_discriminator):
    assert len(set(STOP_AT_100)) == len(STOP_AT_100)
    assert [x for x in ordered_discriminator] == [1, 2, 3, 4, 5, 6, 7]


def test_discriminator(STOP_AT_100):
    d = Discriminator(seed=0, position=0, start=1, stop=100)
    for expected in STOP_AT_100:
        assert d.next() == expected
    with pytest.raises(StopIteration):
        d.next()


def test_assigned(ordered_discriminator):
    d = ordered_discriminator
    d.assign_requested_discriminator(2)
    with pytest.raises(KeyError):
        d.assign_requested_discriminator(2)
    d.assign_requested_discriminator(5)
    d.assign_requested_discriminator(6)
    assert [x for x in d] == [1, 3, 4, 7]
    with pytest.raises(StopIteration):
        d.next()


def test_released(ordered_discriminator):
    d = ordered_discriminator
    assert d.next() == 1
    assert d.next() == 2
    d.release_requested_discriminator(2)
    assert [x for x in d] == [3, 4, 5, 6, 7, 2]
    d.release_requested_discriminator(4)
    with pytest.raises(KeyError):
        d.release_requested_discriminator(4)


client = TestClient(app)


def test_api():
    r = client.post("/discriminator/request", json={"string": "perks"})
    assert r.status_code == 200
    r = client.post("/discriminator/request", json={"string": "hello#"})
    assert r.status_code == 422
    r = client.post("/discriminator/request", json={"string": "hello@"})
    assert r.status_code == 422
    r = client.post("/discriminator/request", json={"string": "h"})
    assert r.status_code == 422


# def test_reconstruction():
#     pass


if __name__ == "__main__":
    pytest.main()
