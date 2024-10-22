import logging

from httpx import AsyncClient

from app.common.exception import InternalServerException

from ..config import emqx_settings
from ..dto.emqx_rule_dto import EmqxCreateRuleDto, EmqxUpdateRuleDto

logger = logging.getLogger(__name__)


class EmqxRuleService:
    def __init__(self) -> None:
        self._url: str = f"{emqx_settings.API_URL}/rules"

    async def create_rule(self, *, dto: EmqxCreateRuleDto) -> None:
        async with AsyncClient(auth=emqx_settings.BASIC_AUTH) as client:
            response = await client.post(self._url, json=dto.model_dump())

            if response.status_code not in (200, 201):
                raise InternalServerException(message="Error while creating rule")

    async def update_rule(self, *, rule_id: str, dto: EmqxUpdateRuleDto) -> None:
        async with AsyncClient(auth=emqx_settings.BASIC_AUTH) as client:
            response = await client.put(f"{self._url}/{rule_id}", json=dto.model_dump())

            if response.status_code not in (200, 201):
                raise InternalServerException(message="Error while updating rule")

    async def delete_rule(self, *, rule_id: str) -> None:
        async with AsyncClient(auth=emqx_settings.BASIC_AUTH) as client:
            response = await client.delete(f"{self._url}/{rule_id}")

            if response.status_code != 204:
                raise InternalServerException(message="Error while deleting rule")
