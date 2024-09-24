import logging

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError

from app.common.dto import ErrorDto
from app.common.exception.base import ViotHttpException
from app.common.exception.constant import MessageError
from app.common.fastapi.serializer import JSONResponse
from app.config import app_settings

logger = logging.getLogger(__name__)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(RequestValidationError)
    async def handle_request_validation_error(  # type: ignore
        request: Request, exc: RequestValidationError
    ) -> JSONResponse[ErrorDto]:
        logger.debug(f"Validation error: {exc.errors()}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=ErrorDto(
                status=status.HTTP_400_BAD_REQUEST,
                error_code=MessageError.VALIDATION_ERROR,
                message=jsonable_encoder(exc.errors()),
            ),
        )

    @app.exception_handler(ViotHttpException)
    async def handle_viot_http_exception(  # type: ignore
        request: Request, exc: ViotHttpException
    ) -> JSONResponse[ErrorDto]:
        logger.debug(f"Viot HTTP exception: {exc.code} - {exc.message}")
        return JSONResponse(
            status_code=exc.STATUS_CODE,
            content=ErrorDto(
                status=exc.STATUS_CODE,
                error_code=exc.code,
                message=exc.message,
            ),
        )

    @app.exception_handler(Exception)
    async def handle_exception(request: Request, exc: Exception) -> JSONResponse[ErrorDto]:  # type: ignore
        logger.error(f"Exception: {exc}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ErrorDto(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                error_code=MessageError.INTERNAL_SERVER_ERROR,
                message=str(exc) if app_settings.ENV == "dev" else "Something went wrong",
            ),
        )
