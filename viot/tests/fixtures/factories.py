import uuid
from collections.abc import Callable, Coroutine
from datetime import UTC, datetime
from typing import Any

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.module.auth.constants import ViotUserRole
from app.module.auth.model.password_reset import PasswordReset
from app.module.auth.model.user import User
from app.module.auth.utils.password_utils import hash_password

last_user = 0


@pytest_asyncio.fixture(scope="function")  # type: ignore
async def user_factory(
    async_session: AsyncSession,
) -> Callable[..., Coroutine[Any, Any, User]]:
    async def create_user(**kwargs: Any) -> User:
        global last_user
        last_user += 1
        user = User(
            first_name=kwargs.get("first_name") or f"First name {last_user}",
            last_name=kwargs.get("last_name") or f"Last name {last_user}",
            email=kwargs.get("email") or f"test_{last_user}@test.com",
            password=hash_password(kwargs.get("password") or "!Test1234"),
            role=kwargs.get("role") or ViotUserRole.USER,
            disabled=kwargs.get("disabled") or False,
        )
        if kwargs.get("teams"):
            user.teams = kwargs.get("teams")  # type: ignore
        if kwargs.get("email_verified_at"):
            user.email_verified_at = kwargs.get("email_verified_at")
        else:
            user.email_verified_at = datetime.now(UTC)

        async_session.add(user)
        await async_session.commit()
        return user

    return create_user


@pytest_asyncio.fixture(scope="function")  # type: ignore
async def password_reset_factory(
    async_session: AsyncSession,
) -> Callable[..., Coroutine[Any, Any, PasswordReset]]:
    async def create_password_reset(**kwargs: Any) -> PasswordReset:
        password_reset = PasswordReset(
            email=kwargs.get("email") or "test@test.com",
            token=kwargs.get("token") or str(uuid.uuid4()),
        )
        created_at = kwargs.get("created_at")
        if created_at:
            password_reset.created_at = created_at
        else:
            password_reset.created_at = datetime.now(UTC)
        async_session.add(password_reset)
        await async_session.commit()
        return password_reset

    return create_password_reset
