from app.common.exception import UnauthorizedException


# JWT
class TokenExpiredException(UnauthorizedException):
    def __init__(self) -> None:
        super().__init__(
            code="TOKEN_EXPIRED",
            message="The provided token has expired",
        )


class InvalidTokenException(UnauthorizedException):
    def __init__(self) -> None:
        super().__init__(
            code="INVALID_TOKEN",
            message="The provided token is invalid",
        )


class InvalidRefreshTokenException(UnauthorizedException):
    def __init__(self) -> None:
        super().__init__(
            code="INVALID_REFRESH_TOKEN",
            message="The provided refresh token is invalid. Please log in again.",
        )
