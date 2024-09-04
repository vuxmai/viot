import asyncio
from datetime import timedelta
from typing import Any

from httpx import AsyncClient

from app.config import app_settings
from app.module.auth.constants import ViotUserRole
from app.module.auth.model.user import User
from app.module.auth.utils.jwt_utils import create_jwt_token, parse_jwt_token


async def test_login_200(client: AsyncClient, user_factory: Any) -> None:
    # given
    user: User = await user_factory(password="!Test1234")

    # when
    response = await client.post("/auth/login", json={"email": user.email, "password": "!Test1234"})
    content = response.json()

    # then
    assert response.status_code == 200
    assert content["accessToken"]
    assert content["refreshToken"]
    assert content["accessTokenExpiresAt"]
    token = parse_jwt_token(content["accessToken"])
    assert token["sub"] == str(user.id)

    assert response.cookies.get("refreshToken")


async def test_login_422_when_invalid_password(client: AsyncClient) -> None:
    # given

    # when
    response = await client.post(
        "/auth/login",
        json={"email": "not_existing_email@test.com", "password": "invalid password"},
    )

    # then
    assert response.status_code == 422


async def test_login_401_when_wrong_password(client: AsyncClient, user_factory: Any) -> None:
    # given
    user: User = await user_factory(password="!Test1234")

    # when
    response = await client.post(
        "/auth/login", json={"email": user.email, "password": "!Test1234" + "123"}
    )
    content = response.json()

    # then
    assert response.status_code == 401
    assert content["errorCode"] == "INVALID_CREDENTIALS"
    assert content["message"] == "The provided credentials are incorrect"


async def test_register_201(client: AsyncClient) -> None:
    # given
    data: dict[str, str] = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "password": "!Test1234",
    }

    # when
    response = await client.post("/auth/register", json=data)
    content = response.json()

    # then
    assert response.status_code == 201
    assert content["id"]
    assert content["firstName"] == data["first_name"]
    assert content["lastName"] == data["last_name"]
    assert content["email"] == data["email"]
    assert content["role"] == ViotUserRole.USER.value
    assert content["createdAt"]
    assert content["updatedAt"] is None


async def test_register_400_when_email_already_exists(
    client: AsyncClient, user_factory: Any
) -> None:
    # given
    user: User = await user_factory()
    data: dict[str, str] = {
        "first_name": "John",
        "last_name": "Doe",
        "email": user.email,
        "password": "!Test1234",
    }

    # when
    response = await client.post("/auth/register", json=data)
    content = response.json()

    # then
    assert response.status_code == 400
    assert content["errorCode"] == "BAD_REQUEST"
    assert content["message"] == "A user with this email already exists"


async def test_verify_email_307_redirect(client: AsyncClient, user_factory: Any) -> None:
    # given
    user: User = await user_factory()
    token, _ = create_jwt_token(
        payload={"user_id": str(user.id)}, expire_duration=timedelta(seconds=1000)
    )

    # when
    response = await client.get(f"/auth/verify-email?token={token}")

    # then
    assert response.status_code == 307
    assert response.headers.get("location") == f"{app_settings.UI_URL}/login"


async def test_verify_email_400_when_invalid_token(client: AsyncClient) -> None:
    # given
    token = "123456"

    # when
    response = await client.get(f"/auth/verify-email?token={token}")
    content = response.json()

    # then
    assert response.status_code == 400
    assert content["errorCode"] == "BAD_REQUEST"
    assert content["message"] == "The provided verify email token is invalid"


async def test_verify_email_400_when_expired_token(client: AsyncClient, user_factory: Any) -> None:
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
