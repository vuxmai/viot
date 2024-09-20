import uuid
from collections.abc import Callable, Coroutine
from datetime import UTC, datetime
from typing import Any
from uuid import UUID

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.module.auth.constants import ViotUserRole
from app.module.auth.model.password_reset import PasswordReset
from app.module.auth.model.user import User
from app.module.auth.utils.password_utils import hash_password
from app.module.device.constants import DeviceStatus, DeviceType, UplinkProtocol
from app.module.device.model.device import Device, Gateway, SubDevice

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


last_device = 0


@pytest_asyncio.fixture(scope="function")  # type: ignore
async def device_factory(
    async_session: AsyncSession,
) -> Callable[..., Coroutine[Any, Any, Device]]:
    async def create_device(team_id: UUID, **kwargs: Any) -> Device:
        global last_device
        last_device += 1

        device = Device(
            name=kwargs.get("name") or f"Test Device {last_device}",
            description=kwargs.get("description") or "Test Device Description",
            device_type=kwargs.get("device_type") or DeviceType.DEVICE,
            team_id=team_id,
        )
        device.status = kwargs.get("status") or DeviceStatus.OFFLINE
        device.image_url = kwargs.get("image_url")
        device.disabled = kwargs.get("disabled") or False
        device.last_connection = kwargs.get("last_connection")
        device.meta_data = kwargs.get("meta_data") or {}
        async_session.add(device)
        await async_session.commit()
        return device

    return create_device


last_gateway = 0


@pytest_asyncio.fixture(scope="function")  # type: ignore
async def gateway_factory(
    async_session: AsyncSession,
) -> Callable[..., Coroutine[Any, Any, Gateway]]:
    async def create_gateway(team_id: UUID, **kwargs: Any) -> Gateway:
        global last_gateway
        last_gateway += 1
        gateway = Gateway(
            name=kwargs.get("name") or f"Test Gateway {last_gateway}",
            description=kwargs.get("description") or "Test Gateway Description",
            device_type=kwargs.get("device_type") or DeviceType.GATEWAY,
            team_id=team_id,
        )
        gateway.status = kwargs.get("status") or DeviceStatus.OFFLINE
        gateway.image_url = kwargs.get("image_url")
        gateway.disabled = kwargs.get("disabled") or False
        gateway.last_connection = kwargs.get("last_connection")
        gateway.meta_data = kwargs.get("meta_data") or {}
        async_session.add(gateway)
        await async_session.commit()
        return gateway

    return create_gateway


last_sub_device = 0


@pytest_asyncio.fixture(scope="function")  # type: ignore
async def sub_device_factory(
    async_session: AsyncSession,
) -> Callable[..., Coroutine[Any, Any, SubDevice]]:
    async def create_sub_device(
        team_id: UUID, gateway_id: UUID, uplink_protocol: UplinkProtocol, **kwargs: Any
    ) -> SubDevice:
        global last_sub_device
        last_sub_device += 1
        sub_device = SubDevice(
            name=kwargs.get("name") or f"Test Sub Device {last_sub_device}",
            description=kwargs.get("description") or "Test Sub Device Description",
            device_type=kwargs.get("device_type") or DeviceType.SUB_DEVICE,
            uplink_protocol=uplink_protocol,
            team_id=team_id,
            gateway_id=gateway_id,
        )
        sub_device.status = kwargs.get("status") or DeviceStatus.OFFLINE
        sub_device.image_url = kwargs.get("image_url")
        sub_device.disabled = kwargs.get("disabled") or False
        sub_device.last_connection = kwargs.get("last_connection")
        sub_device.meta_data = kwargs.get("meta_data") or {}
        async_session.add(sub_device)
        await async_session.commit()
        return sub_device

    return create_sub_device
