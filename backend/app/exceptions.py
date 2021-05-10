# Todo: Exceptions are currently a mess. Clean up.

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

    def __init__(self, status_code=None, detail=None):
        """ Base Exception for all errors from Tusky """
        # Todo: automatically log errors
        if status_code:
            self.status_code = status_code
        if detail:
            self.detail = detail
        super().__init__(status_code=self.status_code, detail=self.detail)

    status_code: int
    detail = "Something went wrong."


########################################################################################
class AuthenticationError(TuskyError):
    """ Base exception for errors resulting from authentication """

    status_code = status.HTTP_400_BAD_REQUEST


class Http400IncorrectPassword(AuthenticationError):
    """ Exception raised when a user's password does not match """

    detail = "Incorrect username or password."


class Http400InactiveUser(AuthenticationError):

    detail = "Inactive user."


########################################################################################
class Http404InvalidRequestError(TuskyError):
    """ Base exceptions for errors deriving from sqlalchemy's Invalid Request Errors. """

    status_code = status.HTTP_404_NOT_FOUND
    detail = "No result found."


class Http404UserNotFound(Http404InvalidRequestError):
    """ Exception raised when a user is not found in the database. """

    detail = "The requested user could not be found."


class Http404ActiveRoomNotFound(Http404InvalidRequestError):
    """ Exception raised when an active room is not in the database. """

    detail = "The requested room does not exist or is no longer active."


class Http404QuizNotFound(Http404InvalidRequestError):
    """ Exception raised when a quiz is not found in the database. """

    detail = "The requested quiz could not be found"


class IntegrityError(TuskyError):
    status_code = status.HTTP_403_FORBIDDEN


class Http403QuizNameConflict(IntegrityError):
    detail = ("Two quizzes by the same owner cannot have the same name.",)
