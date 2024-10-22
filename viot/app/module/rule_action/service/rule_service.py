import json
from uuid import UUID

from injector import inject

from app.database.repository import Filter, Pageable
from app.module.device.constants import DeviceType
from app.module.device.service.device_service import DeviceService
from app.module.emqx.dto.emqx_rule_dto import (
    EmqxActionDto,
    EmqxCreateRuleDto,
    EmqxUpdateRuleDto,
    RepublishArgsDto,
)
from app.module.emqx.service.emqx_rule_service import EmqxRuleService
from app.module.team.service.team_service import TeamService

from ..constants import MQTT_PRIVATE_TRIGGER_TOPIC
from ..dto.rule_dto import RuleCreateDto, RulePagingDto, RuleResponseDto, RuleUpdateDto
from ..exception.rule_exception import RuleNotFoundException
from ..model.action import Action
from ..model.rule import Rule
from ..repository.rule_repository import RuleRepository
from .emqx_rule_builder_service import EmqxRuleBuilderService


class RuleService:
    @inject
    def __init__(
        self,
        rule_repository: RuleRepository,
        emqx_rule_service: EmqxRuleService,
        team_service: TeamService,
        device_service: DeviceService,
        emqx_rule_builder_service: EmqxRuleBuilderService,
    ) -> None:
        self._rule_repository = rule_repository
        self._emqx_rule_service = emqx_rule_service
        self._team_service = team_service
        self._device_service = device_service
        self._emqx_rule_builder_service = emqx_rule_builder_service

    async def get_rule_by_id_and_team_id(self, *, team_id: UUID, rule_id: UUID) -> RuleResponseDto:
        rule = await self._rule_repository.find_by_team_id_and_rule_id(
            team_id=team_id, rule_id=rule_id
        )
        if rule is None:
            raise RuleNotFoundException(rule_id=str(rule_id))

        return RuleResponseDto.from_model(rule)

    async def get_paging_rules(
        self, *, team_id: UUID, device_id: UUID | None, page: int, page_size: int
    ) -> RulePagingDto:
        filters = [Filter("team_id", "eq", team_id)]
        if device_id:
            filters.append(Filter("device_id", "eq", device_id))

        rule_pages = await self._rule_repository.find_all_with_paging(
            pageable=Pageable(page=page, page_size=page_size, filters=filters), use_unique=True
        )
        return RulePagingDto.from_page(rule_pages)

    async def create_rule(
        self, *, team_id: UUID, rule_create_dto: RuleCreateDto
    ) -> RuleResponseDto:
        await self._team_service.check_team_exists_by_id(team_id=team_id)
        device = await self._device_service.get_device_by_id_and_team_id(
            device_id=rule_create_dto.device_id, team_id=team_id
        )

        is_sub_device = device.device_type == DeviceType.SUB_DEVICE
        mqtt_topic = self._emqx_rule_builder_service.get_mqtt_topic(
            event_type=rule_create_dto.event_type,
            is_sub_device=is_sub_device,
        )
        emqx_sql = self._emqx_rule_builder_service.build_sql(
            device_id=rule_create_dto.device_id,
            is_sub_device=is_sub_device,
            topic=mqtt_topic,
            condition=rule_create_dto.condition,
        )

        actions: list[Action] = [
            Action(
                name=action.name,
                description=action.description,
                action_type=action.action_type,
                config=action.config.model_dump(),
                team_id=team_id,
            )
            for action in rule_create_dto.actions
        ]

        rule = Rule(
            name=rule_create_dto.name,
            description=rule_create_dto.description,
            enable=rule_create_dto.enable,
            event_type=rule_create_dto.event_type,
            topic=mqtt_topic,
            sql=emqx_sql,
            device_id=rule_create_dto.device_id,
            team_id=team_id,
            condition=rule_create_dto.condition.model_dump(),
            actions=actions,
        )
        rule = await self._rule_repository.save(rule)

        emqx_rule_dto = EmqxCreateRuleDto(
            id=str(rule.id),
            sql=rule.sql,
            actions=[self._create_emqx_action_dto(rule)],
            enable=rule.enable,
        )
        await self._emqx_rule_service.create_rule(dto=emqx_rule_dto)

        return RuleResponseDto.from_model(rule)

    async def update_rule(
        self, *, team_id: UUID, rule_id: UUID, rule_update_dto: RuleUpdateDto
    ) -> RuleResponseDto:
        rule = await self._rule_repository.find_by_team_id_and_rule_id(
            team_id=team_id, rule_id=rule_id
        )
        if rule is None:
            raise RuleNotFoundException(rule_id=str(rule_id))

        device = await self._device_service.get_device_by_id_and_team_id(
            device_id=rule_update_dto.device_id, team_id=team_id
        )

        is_sub_device = device.device_type == DeviceType.SUB_DEVICE
        mqtt_topic = self._emqx_rule_builder_service.get_mqtt_topic(
            event_type=rule_update_dto.event_type,
            is_sub_device=is_sub_device,
        )
        emqx_sql = self._emqx_rule_builder_service.build_sql(
            device_id=rule_update_dto.device_id,
            is_sub_device=is_sub_device,
            topic=mqtt_topic,
            condition=rule_update_dto.condition,
        )

        existing_actions_map: dict[UUID, Action] = {action.id: action for action in rule.actions}
        actions: list[Action] = []

        for action_update in rule_update_dto.actions:
            if action_update.id in existing_actions_map:
                existing_action = existing_actions_map[action_update.id]
                existing_action.name = action_update.name
                existing_action.description = action_update.description
                existing_action.action_type = action_update.action_type
                existing_action.config = action_update.config.model_dump()
                actions.append(existing_action)
            else:
                actions.append(
                    Action(
                        name=action_update.name,
                        description=action_update.description,
                        action_type=action_update.action_type,
                        config=action_update.config.model_dump(),
                        team_id=team_id,
                    )
                )

        rule.name = rule_update_dto.name
        rule.description = rule_update_dto.description
        rule.enable = rule_update_dto.enable
        rule.event_type = rule_update_dto.event_type
        rule.topic = mqtt_topic
        rule.sql = emqx_sql
        rule.device_id = rule_update_dto.device_id
        rule.condition = rule_update_dto.condition.model_dump()
        rule.actions = actions

        rule = await self._rule_repository.save(rule)

        emqx_rule_dto = EmqxUpdateRuleDto(
            sql=rule.sql,
            actions=[self._create_emqx_action_dto(rule)],
            enable=rule.enable,
        )
        await self._emqx_rule_service.update_rule(rule_id=str(rule.id), dto=emqx_rule_dto)

        return RuleResponseDto.from_model(rule)

    def _create_emqx_action_dto(self, rule: Rule) -> EmqxActionDto:
        return EmqxActionDto(
            function="republish",
            args=RepublishArgsDto(
                topic=MQTT_PRIVATE_TRIGGER_TOPIC,
                qos=2,
                retain=True,
                direct_dispatch=True,
                payload=json.dumps(
                    {
                        "device_id": str(rule.device_id),
                        "rule_id": str(rule.id),
                        "action_ids": [str(action.id) for action in rule.actions],
                        "ts": "${ts}",
                        "payload": "${payload}",
                    }
                ),
            ),
        )

    async def delete_rule(self, *, team_id: UUID, rule_id: UUID) -> None:
        await self._rule_repository.delete_by_team_id_and_rule_id(team_id=team_id, rule_id=rule_id)
        await self._emqx_rule_service.delete_rule(rule_id=str(rule_id))
