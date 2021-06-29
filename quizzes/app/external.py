import datetime

import httpx


class Snowflake(int):
    _bit_length_time = 39
    _bit_length_sequence = 11
    _bit_length_machine_id = 13

    _TUSKY_EPOCH = datetime.datetime(year=2020, month=9, day=1).timestamp()

    @property
    def time(self) -> datetime.datetime:
        time_part = self >> (self._bit_length_sequence + self._bit_length_machine_id)
        return datetime.datetime.fromtimestamp(time_part + self._TUSKY_EPOCH)


async def get_snowflake() -> Snowflake:
    async with httpx.AsyncClient() as client:
        r = await client.get("http://host.docker.internal:8080")
    r.raise_for_status()
    return Snowflake(r.json()["id"])
