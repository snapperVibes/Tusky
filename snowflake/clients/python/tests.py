from typing import NamedTuple

import pytest

from .__init__ import Snowflake


class P(NamedTuple):
    actual: Snowflake
    eq: int
    id: int
    machine_id: int
    msb: int
    seq: int
    time: int


params = [
    # P(
    #     actual=Snowflake(43614351732936700),
    #     eq=43614351732936700,
    #     id=43614351732936700,
    #     machine_id=1234,
    #     msb=0,
    #     seq=0,
    #     time=2599617942
    # ),
    # P(
    #     actual=Snowflake(43615569960144900),
    #     eq=43615569960144900,
    #     id=43615569960144900,
    #     machine_id=1234,
    #     msb=0,
    #     seq=0,
    #     time=2599690554
    # ),
    P(
        actual=Snowflake(43615771219628030),
        eq=43615771219628030,
        id=43615771219628030,
        machine_id=1234,
        msb=0,
        seq=0,
        time=2599702550
    )
]


@pytest.mark.parametrize("p", params)
def test_eq(p: P):
    assert p.actual == p.eq


@pytest.mark.parametrize("p", params)
def test_id(p: P):
    assert p.actual.id == p.id


@pytest.mark.parametrize("p", params)
def test_machine_id(p: P):
    assert p.actual.machine_id == p.machine_id


@pytest.mark.parametrize("p", params)
def test_msb(p: P):
    assert p.actual.msb == p.msb


@pytest.mark.parametrize("p", params)
def test_sequence(p: P):
    assert p.actual.sequence == p.seq


@pytest.mark.parametrize("p", params)
def test_time(p: P):
    assert p.actual.time == p.time


if __name__ == "__main__":
    pytest.main()
