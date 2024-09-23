import asyncio
from datetime import datetime, timedelta
from typing import Any

from httpx import AsyncClient

from app.config import app_settings
from app.module.auth.constants import FORGOT_PASSWORD_DURATION_SEC, ViotUserRole
from app.module.auth.model.password_reset import PasswordReset
from app.module.auth.model.user import User
from app.module.auth.utils.jwt_utils import create_jwt_token, parse_jwt_token
from tests.utils.user_token import get_user_token


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


async def test_logout_204(client: AsyncClient, user_factory: Any) -> None:
    # given
    user: User = await user_factory(password="!Test1234")
    user_token = await get_user_token(client, user, "!Test1234")

    # when
    client.cookies.set("refreshToken", user_token.refresh_token)
    response = await client.post(
        "/auth/logout",
        headers={"Authorization": f"Bearer {user_token.access_token}"},
    )

    # then
    assert response.status_code == 204
    assert "refreshToken" not in response.cookies


async def test_refresh_200(client: AsyncClient, user_factory: Any) -> None:
    # given
    user: User = await user_factory(password="!Test1234")
    user_token = await get_user_token(client, user, "!Test1234")

    # when
    client.cookies.set("refreshToken", user_token.refresh_token)
    response = await client.post("/auth/refresh")
    content = response.json()

    # then
    assert response.status_code == 200
    assert content["accessToken"]
    assert content["refreshToken"]
    assert content["accessTokenExpiresAt"]


# For failed cases refresh token will be fix in the next PR


async def test_forgot_password_204(client: AsyncClient, user_factory: Any) -> None:
    # given
    user: User = await user_factory()

    # when
    response = await client.post("/auth/forgot-password", json={"email": user.email})

    # then
    assert response.status_code == 204


async def test_forgot_password_204_when_email_not_exists(client: AsyncClient) -> None:
    # given
    email = "not_existing_email@test.com"

    # when
    response = await client.post("/auth/forgot-password", json={"email": email})

    # then
    assert response.status_code == 204


async def test_reset_password_204(
    client: AsyncClient, user_factory: Any, password_reset_factory: Any
) -> None:
    # given
    user: User = await user_factory(password="!Test1234")
    password_reset: PasswordReset = await password_reset_factory(email=user.email)
    data = {"token": password_reset.token, "password": "!Test12345678"}

    # when
    response = await client.post("/auth/reset-password", json=data)

    # then
    assert response.status_code == 204


async def test_reset_password_400_when_invalid_token(client: AsyncClient) -> None:
    # given
    token = "123456"
    data = {"token": token, "password": "!Test12345678"}

    # when
    response = await client.post("/auth/reset-password", json=data)
    content = response.json()

    # then
    assert response.status_code == 400
    assert content["errorCode"] == "BAD_REQUEST"
    assert content["message"] == "The provided reset password token is invalid"


async def test_reset_password_400_when_expired_token(
    client: AsyncClient, user_factory: Any, password_reset_factory: Any
) -> None:
    # given
    user: User = await user_factory()
    password_reset: PasswordReset = await password_reset_factory(
        email=user.email,
        created_at=datetime.now() - timedelta(seconds=FORGOT_PASSWORD_DURATION_SEC),
    )
    data = {"token": password_reset.token, "password": "!Test12345678"}

    # when
    response = await client.post("/auth/reset-password", json=data)
    content = response.json()

    # then
    assert response.status_code == 400
    assert content["errorCode"] == "BAD_REQUEST"
    assert content["message"] == "The provided reset password token has expired"


async def test_reset_password_400_when_user_not_exists(
    client: AsyncClient, password_reset_factory: Any
) -> None:
    # given
    password_reset: PasswordReset = await password_reset_factory(email="usernotexists@test.com")
    data = {"token": password_reset.token, "password": "!Test12345678"}

    # when
    response = await client.post("/auth/reset-password", json=data)
    content = response.json()

    # then
    assert response.status_code == 400
    assert content["errorCode"] == "BAD_REQUEST"
    assert content["message"] == "The provided reset password token is invalid"


async def test_reset_password_400_when_duplicate_password(
    client: AsyncClient, user_factory: Any, password_reset_factory: Any
) -> None:
    # given
    user: User = await user_factory(password="!Test1234")
    password_reset: PasswordReset = await password_reset_factory(email=user.email)
    data = {"token": password_reset.token, "password": "!Test1234"}

    # when
    response = await client.post("/auth/reset-password", json=data)
    content = response.json()

    # then
    assert response.status_code == 400
    assert content["errorCode"] == "BAD_REQUEST"
    assert content["message"] == "New password must be different from the current password"
