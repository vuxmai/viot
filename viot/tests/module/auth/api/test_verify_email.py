import asyncio
from datetime import timedelta
from typing import Any

from httpx import AsyncClient

from app.config import settings
from app.module.auth.utils import create_jwt_token
from app.module.user.model import User


async def test_307_redirect(client: AsyncClient, user_factory: Any) -> None:
    # given
    user: User = await user_factory()
    token, _ = create_jwt_token(
        payload={"user_id": str(user.id)}, expire_duration=timedelta(seconds=1000)
    )

    # when
    response = await client.get(f"/auth/verify-email?token={token}")

    # then
    assert response.status_code == 307
    assert response.headers.get("location") == f"{settings.UI_URL}/login"


async def test_400_when_invalid_token(client: AsyncClient) -> None:
    # given
    token = "123456"

    # when
    response = await client.get(f"/auth/verify-email?token={token}")
    content = response.json()

    # then
    assert response.status_code == 400
    assert content["errorCode"] == "BAD_REQUEST"
    assert content["message"] == "The provided verify email token is invalid"


async def test_400_when_expired_token(client: AsyncClient, user_factory: Any) -> None:
    # given
    user: User = await user_factory()
    token = create_jwt_token(
        payload={"user_id": str(user.id)}, expire_duration=timedelta(seconds=1)
    )
    await asyncio.sleep(1)

    # when
    response = await client.get(f"/auth/verify-email?token={token}")
    content = response.json()

    # then
    assert response.status_code == 400
    assert content["errorCode"] == "BAD_REQUEST"
    assert content["message"] == "The provided verify email token is invalid"
