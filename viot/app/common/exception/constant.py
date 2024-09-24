from typing import Any

from app.common.dto import ErrorDto


class MessageError:
    INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"
    BAD_REQUEST = "BAD_REQUEST"
    UNAUTHORIZED = "UNAUTHORIZED"
    PERMISSION_DENIED = "PERMISSION_DENIED"
    NOT_FOUND = "NOT_FOUND"
    CONFLICT = "CONFLICT"
    TOO_MANY_REQUESTS = "TOO_MANY_REQUESTS"
    VALIDATION_ERROR = "VALIDATION_ERROR"


class MessageErrorExample:
    BAD_REQUEST = "Invalid UUID format: 1234567890"
    UNAUTHORIZED = "Authentication failed"
    PERMISSION_DENIED = "You don't have permission to perform this operation!"
    NOT_FOUND = "Requested item wasn't found!"
    TOO_MANY_REQUESTS = "Too Many Requests for current user"
    VALIDATION_ERROR = "field required"


RESPONSE_SCHEMAS: dict[int | str, dict[str, Any]] = {
    400: {
        "model": ErrorDto,
        "content": {
            "application/json": {
                "example": {
                    "status": 400,
                    "errorCode": MessageError.BAD_REQUEST,
                    "message": MessageErrorExample.BAD_REQUEST,
                }
            }
        },
    },
    401: {
        "model": ErrorDto,
        "content": {
            "application/json": {
                "example": {
                    "status": 401,
                    "errorCode": MessageError.UNAUTHORIZED,
                    "message": MessageErrorExample.UNAUTHORIZED,
                }
            }
        },
    },
    403: {
        "model": ErrorDto,
        "content": {
            "application/json": {
                "example": {
                    "status": 403,
                    "errorCode": MessageError.PERMISSION_DENIED,
                    "message": MessageErrorExample.PERMISSION_DENIED,
                }
            }
        },
    },
    404: {
        "model": ErrorDto,
        "content": {
            "application/json": {
                "example": {
                    "status": 404,
                    "errorCode": MessageError.NOT_FOUND,
                    "message": MessageErrorExample.NOT_FOUND,
                }
            }
        },
    },
    429: {
        "model": ErrorDto,
        "content": {
            "application/json": {
                "example": {
                    "status": 429,
                    "errorCode": MessageError.TOO_MANY_REQUESTS,
                    "message": MessageErrorExample.TOO_MANY_REQUESTS,
                }
            }
        },
    },
}
