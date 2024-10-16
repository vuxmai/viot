from typing import Any, Literal
from uuid import UUID

from pydantic import BaseModel

from app.common.dto import BaseInDto


class EmqxAuthenRequestDto(BaseInDto):
    device_id: UUID
    username: str
    password: str
    ip_address: str


class EmqxAuthenResponseDto(BaseModel):
    # Because emqx use snake_case so we dont use BaseOutDto
    # We don't return result `ignore` to avoid continue authentication chain

    result: Literal["allow", "deny"]
    is_superuser: bool = False
    client_attrs: dict[str, Any] = {}  # Since EMQX v5.7.0
    acl: list[dict[str, Any]] = []  # Since EMQX v5.8.0
