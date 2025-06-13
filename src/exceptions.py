from http import HTTPStatus


class AppError(Exception):
    """Class Default to Error in application."""
    status: int


class BadRequest(AppError):
    status = HTTPStatus.BAD_REQUEST


class NotFound(AppError):
    status = HTTPStatus.NOT_FOUND


class ErrorPartnerGreaterEqual500(AppError):
    status = HTTPStatus.INTERNAL_SERVER_ERROR


class ErrorPartnerGreaterEqual400(AppError):
    status = HTTPStatus.BAD_REQUEST


class ErrorRequests(AppError):
    status = HTTPStatus.INTERNAL_SERVER_ERROR


class ParamInvalid(AppError):
    status = HTTPStatus.BAD_REQUEST


class ObjectNotFound(AppError):
    status = HTTPStatus.NOT_FOUND
