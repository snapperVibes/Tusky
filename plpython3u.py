__all__ = "plpython"
from typing import NamedTuple, Sequence, Callable


class PlPythonManager:
    """"""

    # Keep in mind: "Reflection is never clever." https://go-proverbs.github.io/
    #  Unfortunately, reflection (introspection) seems like the best way
    #  to ensure the code on the server and in the database remain identical.
    def __init__(self):
        objects_to_copy: Sequence[Callable]

    class ObjectToCopy(NamedTuple):
        """
        Some Python functions are shared between the server and database.
        To avoid repeating code (and accidentally ending up with different implementations),
        shared functions are added to the PlPython3u Global Dictionary.
        The functions are then callable from PlPython3u by using `GD["func_name"](arguments)`
        """

        name: str
        body: str

    def register(self, f: Callable):
        """ Registers a function-like object to have its source copied to the PlPython Global Dictionary """


plpython_verison = DDL(
    """\
CREATE OR REPLACE FUNCTION plpython_version()
RETURNS TEXT as $$
import sys
return sys.version
$$ LANGUAGE plpython3u
"""
)

event.listen(
    User.__table__, "after_create", plpython_verison.execute_if(dialect="postgresql")
)
