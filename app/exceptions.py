# Todo: Make work as type
from typing import Any, Optional


class Result:
    """ Wraps objects that may raise exception """
    __slots__ = ["Ok", "Err"]

    def __init__(self, ok: Any = None, err: Optional[BaseException] = None):
        self.Ok = ok
        self.Err = err

    def unwrap(self):
        if self.Err:
            raise self.Err
        return self.Ok


class TuskyError(BaseException):
    """
    Base Exception for the Tusky application.
    In general, exceptions should not be raised directly. Instead, they should be wrapped in a Result.
    """
    def __init__(self):
        """ Automatically logs errors """
        pass


class AuthenticationError(TuskyError):
    """ Base exception for errors resulting from authentication """


class UserDoesNotExist(AuthenticationError):
    """ Exception raised when user not found in database """
    def __init__(self, username, number):
        pass


class IncorrectPassword(AuthenticationError):
    """ Exception raised when a user's password does not match """
    def __init__(self, username, number):
        pass
