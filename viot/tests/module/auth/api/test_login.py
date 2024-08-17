from typing import Any

from httpx import AsyncClient

from app.module.auth.utils import parse_jwt_token
from app.module.user.model import User


async def test_200(client: AsyncClient, user_factory: Any) -> None:
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
    assert content["refreshTokenExpiresAt"]
    token = parse_jwt_token(content["accessToken"])
    assert token["sub"] == str(user.id)

    assert response.cookies.get("refreshToken")


async def test_422_when_invalid_password(client: AsyncClient) -> None:
    # given

    # when
    response = await client.post(
        "/auth/login",
        json={"email": "not_existing_email@test.com", "password": "invalid password"},
    )

    # then
    assert response.status_code == 422


async def test_401_when_wrong_password(client: AsyncClient, user_factory: Any) -> None:
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
