__all__ = ["get_id"]
from numbers import Number


class Snowflake:
    def __init__(self, value: int):
        # self._byteorder = sys.byteorder
        # b = value.to_bytes(8, self._byteorder)
        # self.ok = bytearray(b)
        self._value = value


    @property
    def id(self):
        pass

    @property
    def machine_id(self):
        # return self._bytes & (self._mask_machine_id >> self._bit_length_sequence)
        # return self._bytes & b"5"
        pass

    @property
    def msb(self):
        pass
        # return self._bytes >> 63

    @property
    def sequence(self):
        pass
        # return self._bytes & self._mask_sequence

    @property
    def time(self):
        # return self._bytes >> (self._bit_length_sequence + self._bit_length_machine_id)
        pass

    _bit_length_time = 39
    _bit_length_sequence = 11
    _bit_length_machine_id = 13

    _mask_machine_id = 1 << (_bit_length_machine_id - 1) << _bit_length_sequence
    _mask_sequence = 1024  # 1 << _bit_length_sequence - 1

    def __eq__(self, other):
        if isinstance(other, Number):
            return self._value == other
        elif isinstance(other, Snowflake):
            return self._value == other._value




x = Snowflake(43615771219628030)
# print("Machine id: ", x.machine_id, "\t (1234)")
# print("Seq: ", x.sequence, "\t(0)")
assert x == 43615771219628030
assert x == x
# assert x.time == 2599702550, x.time
print(x)
