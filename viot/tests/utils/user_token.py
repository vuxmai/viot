import msgspec
from httpx import AsyncClient

from app.module.auth.model.user import User


class UserToken(msgspec.Struct):
    access_token: str
    refresh_token: str


async def get_user_token(client: AsyncClient, user: User, password: str) -> UserToken:
    login_data = {
        "email": user.email,
        "password": password,
    }
    response = await client.post("/auth/login", json=login_data)
    content = response.json()
    return UserToken(access_token=content["accessToken"], refresh_token=content["refreshToken"])
