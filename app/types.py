from typing import NamedTuple


# It seems ridicolous to have a whole file for one type,
# but I assume more types will be made as we time passes.
# If production roles around and there's still only this type,
# refactor it somewhere else.
class Role(NamedTuple):
    name: str
    emoji: str


class SnapAPI():
    """ Decorator class whose instances store decorated methods """
    # Todo: Implement (or not, it's a lot of work for just a wrapper)
