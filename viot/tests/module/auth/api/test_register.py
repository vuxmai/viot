from typing import Any

from httpx import AsyncClient

from app.module.user.constant import ViotUserRole
from app.module.user.model import User


async def test_201(client: AsyncClient) -> None:
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


async def test_400_when_email_already_exists(client: AsyncClient, user_factory: Any) -> None:
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
