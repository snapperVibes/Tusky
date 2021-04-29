from typing import Optional

from fastapi import status
from fastapi.exceptions import HTTPException as fastapi_HTTPException
from sqlalchemy.exc import InvalidRequestError as sqlalchemy_InvalidRequestError


class TuskyError(fastapi_HTTPException):
    """
    Base Exception for the Tusky application.
    """

    # Tusky functions should not take or return errors from 3rd party libraries.
    #  This is a stylistic choice to simplify dependency management.
    #  Errors thrown by 3rd party libraries should be wrapped in a Result
    #  (https://github.com/dbrgn/result) and propagated to the api_route,
    #  at which point the Result is raised.
    #  A TuskyError's `detail` attribute is a end-user facing error message.
    #
    #  Be careful: Exceptions (will eventually) be logged.
    #  Don't do anything that (for example)
    #  would expose a plain-text passwords in the logs.
    #
    # Todo: Make a Tusky code-style document
    # Some best practices:
    #   DO:
    #       >>> example_object_ = db.query(example_object_).one()
    #       >>> if example_object_ is None:
    #       >>>     return Err(ExampleDoesNotExist)
    #   DON'T
    #       >>>try:
    #       >>>    example_object_ = db.query(example_object_).one_or_none()
    #       >>>except sqlalchemy_InvalidRequestError as err:
    #       >>>    return Err(ExampleDoesNotExist(from_= err))

    def __init__(self, from_: Optional[BaseException] = None):
        """ Automatically logs errors """
        if from_:
            self.__cause__ = from_
        status_code: int = NotImplemented
        detail = "Something went wrong."


########################################################################################
class AuthenticationError(TuskyError):
    """ Base exception for errors resulting from authentication """

    status_code = status.HTTP_400_BAD_REQUEST


class IncorrectPassword(AuthenticationError):
    """ Exception raised when a user's password does not match """

    detail = "Incorrect username or password."


########################################################################################
class InvalidRequestError(TuskyError):
    """ Base exceptions for errors deriving from sqlalchemy's Invalid Request Errors. """

    status_code = 404
    detail = "No result found."


class UserNotFound(InvalidRequestError):
    """ Exception raised when a user is not found in the database. """

    detail = "The requested user could not be found."


class ActiveRoomNotFound(InvalidRequestError):
    """ Exception raised when an active room is not in the database. """

    detail = "The requested room does not exist or is no longer active."


class QuizNotFound(InvalidRequestError):
    """ Exception raised when a quiz is not found in the database. """

    detail = "The requested quiz could not be found"
