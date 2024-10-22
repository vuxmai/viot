from datetime import datetime
from typing import Any, Literal
from uuid import UUID

from pydantic import Field

from app.common.dto import BaseInDto, BaseOutDto

from ..constants import ActionType
from ..model.action import Action


class ActionEmailConfigDto(BaseInDto):
    email_address: str = Field(..., examples=["user@example.com"])
    # subject: str = Field(..., examples=["Notification"])
    # body: str = Field(..., examples=["This is an email body."])


class ActionWebhookConfigDto(BaseInDto):
    url: str = Field(..., examples=["https://example.com/webhook"])
    method: Literal["POST"] = Field(
        ..., examples=["POST"], description="HTTP method for the webhook."
    )
    headers: dict[str, str | int] | None = Field(
        default=None, examples=[{"Authorization": "Bearer token"}]
    )
    payload: dict[str, Any] | None = Field(default=None, examples=[{"key": "value"}])


class ActionCreateDto(BaseInDto):
    name: str = Field(..., examples=["Send Email Action"])
    description: str | None = Field(default=None, examples=["Send email notification."])
    action_type: ActionType = Field(..., examples=[ActionType.EMAIL])
    config: ActionEmailConfigDto | ActionWebhookConfigDto


class ActionUpdateDto(ActionCreateDto):
    id: UUID


class ActionResponseDto(BaseOutDto):
    id: UUID
    name: str
    description: str | None
    action_type: ActionType
    config: dict[str, Any]
    created_at: datetime
    updated_at: datetime | None

    @classmethod
    def from_model(cls, action: Action) -> "ActionResponseDto":
        return cls(
            id=action.id,
            name=action.name,
            description=action.description,
            action_type=action.action_type,
            config=action.config,
            created_at=action.created_at,
            updated_at=action.updated_at,
        )
