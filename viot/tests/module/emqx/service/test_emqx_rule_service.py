from unittest.mock import AsyncMock, patch
from uuid import uuid4

import pytest

from app.common.exception import InternalServerException
from app.module.emqx.dto.emqx_rule_dto import EmqxCreateRuleDto, EmqxUpdateRuleDto
from app.module.emqx.service.emqx_rule_service import EmqxRuleService


@patch("app.module.emqx.service.emqx_rule_service.AsyncClient")
async def test_create_rule(mock_async_client: AsyncMock) -> None:
    # given
    emqx_service = EmqxRuleService()
    mock_response = mock_async_client.return_value.__aenter__.return_value.post.return_value
    mock_response.status_code = 201

    rule_dto = EmqxCreateRuleDto(
        id="test_rule",
        enable=True,
        sql="SELECT * FROM test",
        actions=[],
    )

    # when
    await emqx_service.create_rule(dto=rule_dto)

    # then
    mock_async_client.return_value.__aenter__.return_value.post.assert_called_once_with(
        f"{emqx_service._url}",  # type: ignore
        json=rule_dto.model_dump(),
    )


@patch("app.module.emqx.service.emqx_rule_service.AsyncClient")
async def test_create_rule_throws_exception_on_failure(mock_async_client: AsyncMock) -> None:
    # given
    emqx_service = EmqxRuleService()
    mock_response = mock_async_client.return_value.__aenter__.return_value.post.return_value
    mock_response.status_code = 500

    rule_dto = EmqxCreateRuleDto(
        id="test_rule",
        enable=True,
        sql="SELECT * FROM test",
        actions=[],
    )
    # when / then
    with pytest.raises(InternalServerException, match="Error while creating rule"):
        await emqx_service.create_rule(dto=rule_dto)


@patch("app.module.emqx.service.emqx_rule_service.AsyncClient")
async def test_update_rule(mock_async_client: AsyncMock) -> None:
    # given
    emqx_service = EmqxRuleService()
    mock_response = mock_async_client.return_value.__aenter__.return_value.put.return_value
    mock_response.status_code = 200

    rule_id = str(uuid4())
    rule_update_dto = EmqxUpdateRuleDto(sql="SELECT * FROM updated_test", actions=[], enable=True)

    # when
    await emqx_service.update_rule(rule_id=rule_id, dto=rule_update_dto)

    # then
    mock_async_client.return_value.__aenter__.return_value.put.assert_called_once_with(
        f"{emqx_service._url}/{rule_id}",  # type: ignore
        json=rule_update_dto.model_dump(),
    )


@patch("app.module.emqx.service.emqx_rule_service.AsyncClient")
async def test_update_rule_throws_exception_on_failure(mock_async_client: AsyncMock) -> None:
    # given
    emqx_service = EmqxRuleService()
    mock_response = mock_async_client.return_value.__aenter__.return_value.put.return_value
    mock_response.status_code = 500

    rule_id = str(uuid4())
    rule_update_dto = EmqxUpdateRuleDto(sql="SELECT * FROM updated_test", actions=[], enable=True)

    # when / then
    with pytest.raises(InternalServerException, match="Error while updating rule"):
        await emqx_service.update_rule(rule_id=rule_id, dto=rule_update_dto)


@patch("app.module.emqx.service.emqx_rule_service.AsyncClient")
async def test_delete_rule(mock_async_client: AsyncMock) -> None:
    # given
    emqx_service = EmqxRuleService()
    mock_response = mock_async_client.return_value.__aenter__.return_value.delete.return_value
    mock_response.status_code = 204

    rule_id = str(uuid4())

    # when
    await emqx_service.delete_rule(rule_id=rule_id)

    # then
    mock_async_client.return_value.__aenter__.return_value.delete.assert_called_once_with(
        f"{emqx_service._url}/{rule_id}"  # type: ignore
    )


@patch("app.module.emqx.service.emqx_rule_service.AsyncClient")
async def test_delete_rule_throws_exception_on_failure(mock_async_client: AsyncMock) -> None:
    # given
    emqx_service = EmqxRuleService()
    mock_response = mock_async_client.return_value.__aenter__.return_value.delete.return_value
    mock_response.status_code = 500

    rule_id = str(uuid4())

    # when / then
    with pytest.raises(InternalServerException, match="Error while deleting rule"):
        await emqx_service.delete_rule(rule_id=rule_id)
