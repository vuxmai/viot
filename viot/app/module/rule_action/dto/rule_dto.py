from datetime import datetime
from typing import Any, Union
from uuid import UUID

from pydantic import Field, field_validator

from app.common.dto import BaseInDto, BaseOutDto, PagingDto
from app.database.repository.pagination import Page

from ..constants import EventType, RuleLogic, RuleOperator
from ..model.rule import Rule
from .action_dto import ActionCreateDto, ActionResponseDto, ActionUpdateDto


class Condition(BaseInDto):
    field: str
    operator: RuleOperator
    value: str | int | bool


class ConditionLogic(BaseInDto):
    logic: RuleLogic
    conditions: list[Union[Condition, "ConditionLogic"]]


class BaseRuleDto(BaseInDto):
    device_id: UUID
    name: str = Field(..., examples=["Temperature Alert Rule"])
    description: str | None = Field(
        default=None, examples=["Alert when temperature exceeds threshold."]
    )
    event_type: EventType
    enable: bool
    condition: ConditionLogic | Condition = Field(
        examples=[
            {
                "logic": RuleLogic.AND,
                "conditions": [
                    {"field": "temperature", "operator": RuleOperator.gt, "value": 37},
                    {"field": "humidity", "operator": RuleOperator.lt, "value": 50},
                ],
            },
            {"field": "temperature", "operator": RuleOperator.gt, "value": 37},
        ]
    )

    @field_validator("condition", mode="before")
    def validate_condition(cls, value: ConditionLogic | Condition) -> ConditionLogic | Condition:
        if isinstance(value, ConditionLogic) and len(value.conditions) < 2:
            raise ValueError("Condition logic must contain at least two sub-conditions.")
        return value


class RuleCreateDto(BaseRuleDto):
    actions: list[ActionCreateDto]


class RuleUpdateDto(BaseRuleDto):
    actions: list[ActionUpdateDto]


class RuleResponseDto(BaseOutDto):
    id: UUID
    device_id: UUID
    name: str
    description: str | None
    enable: bool
    event_type: EventType
    condition: dict[str, Any]
    topic: str
    actions: list[ActionResponseDto]
    created_at: datetime
    updated_at: datetime | None

    @classmethod
    def from_model(cls, rule: Rule) -> "RuleResponseDto":
        return RuleResponseDto(
            id=rule.id,
            device_id=rule.device_id,
            name=rule.name,
            description=rule.description,
            enable=rule.enable,
            event_type=rule.event_type,
            condition=rule.condition,
            topic=rule.topic,
            actions=[ActionResponseDto.from_model(action) for action in rule.actions],
            created_at=rule.created_at,
            updated_at=rule.updated_at,
        )


class RulePagingDto(PagingDto[RuleResponseDto]):
    @classmethod
    def from_page(cls, page: Page[Rule]) -> "RulePagingDto":
        return RulePagingDto(
            items=[RuleResponseDto.from_model(rule) for rule in page.items],
            total_items=page.total_items,
            page=page.page,
            page_size=page.page_size,
        )
