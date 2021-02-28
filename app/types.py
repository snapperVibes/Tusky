from typing import NamedTuple


# It seems ridicolous to have a whole file for one type,
# but I assume more types will be made as we time passes.
# If production roles around and there's still only this type,
# refactor it somewhere else.
class Role(NamedTuple):
    name: str
    emoji: str

identifiers = "ABCDEFGHJKMNPQRSTUVWXYZ123456789"

# In-Memory types for prototyping. If these are useful, they might stick around
class _MockDB:
    pass


db = _MockDB()

db.rooms = {
    "ABCDE": {
        "active": True
    }
}




