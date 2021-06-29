__all__ = ["Snowflake", "get_snowflake"]

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
        # This snowflake implementation increments every 10 milliseconds
        seconds_since_tusky_epoch = time_part / 100
        return datetime.datetime.fromtimestamp(seconds_since_tusky_epoch + self._TUSKY_EPOCH)


async def get_snowflake(uri: str = "http://host.docker.internal:8080") -> Snowflake:
    async with httpx.AsyncClient() as client:
        r = await client.get(uri)
    r.raise_for_status()
    return Snowflake(r.json()["id"])
