from collections.abc import Mapping
from typing import Any, Generic, TypeVar

import msgspec
from fastapi import Response
from fastapi.encoders import jsonable_encoder
from starlette.background import BackgroundTask

from app.common.dto import BaseOutDto

T = TypeVar("T", bound=BaseOutDto | Any | None)


class JSONResponse(Response, Generic[T]):
    """
    JSON response using the high-performance `msgspec` library to serialize data to JSON.
    """

    def __init__(
        self,
        *,
        content: T,
        status_code: int = 200,
        headers: Mapping[str, str] | None = None,
        media_type: str = "application/json",
        background: BackgroundTask | None = None,
    ) -> None:
        super().__init__(content, status_code, headers, media_type, background)

    def render(self, content: T) -> bytes:
        if content is None:
            return b""
        elif isinstance(content, BaseOutDto):  # type: ignore
            return msgspec.json.encode(content.model_dump(by_alias=True))
        else:
            return msgspec.json.encode(jsonable_encoder(content))  # type: ignore

    @classmethod
    def no_content(
        cls,
        *,
        headers: dict[str, str] | None = None,
        background: BackgroundTask | None = None,
    ) -> "JSONResponse[None]":
        if headers is None:
            headers = {}
        headers["content-length"] = "0"
        return cls(content=None, status_code=204, headers=headers, background=background)  # type: ignore
