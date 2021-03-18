from typing import Any, Generic, TypeVar, Union


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
