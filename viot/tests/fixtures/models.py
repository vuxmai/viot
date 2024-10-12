from datetime import UTC, datetime, timedelta
from unittest.mock import Mock
from uuid import uuid4

import pytest
from faker import Faker

from app.module.auth.constants import REFRESH_TOKEN_DURATION_SEC, ViotUserRole
from app.module.auth.model.password_reset import PasswordReset
from app.module.auth.model.permission import Permission
from app.module.auth.model.role import Role
from app.module.auth.model.user import User
from app.module.auth.utils.password_utils import hash_password
from app.module.device.constants import DeviceStatus, DeviceType
from app.module.device.model.device import Device
from app.module.device_data.model.connect_log import ConnectLog
from app.module.team.model.team import Team
from app.module.team.model.team_invitation import TeamInvitation


@pytest.fixture
def mock_user() -> Mock:
    user = Mock(spec=User)
    user.id = uuid4()
    user.first_name = Faker().first_name()
    user.last_name = Faker().last_name()
    user.email = Faker().email()
    user.email_verified_at = datetime.now()
    user.raw_password = "!abcABC123"
    user.password = hash_password("!abcABC123")
    user.role = ViotUserRole.USER
    user.disabled = False
    user.created_at = datetime.now(UTC)
    user.updated_at = None
    user.verified = True
    return user


@pytest.fixture
def mock_refresh_token(mock_user: Mock) -> Mock:
    refresh_token = Mock()
    refresh_token.id = uuid4()
    refresh_token.user_id = mock_user.id
    refresh_token.token = uuid4().hex
    refresh_token.expires_at = datetime.now(UTC) + timedelta(seconds=REFRESH_TOKEN_DURATION_SEC)
    return refresh_token


@pytest.fixture
def mock_password_reset(mock_user: Mock) -> Mock:
    password_reset = Mock(spec=PasswordReset)
    password_reset.email = mock_user.email
    password_reset.token = uuid4().hex
    password_reset.created_at = datetime.now(UTC)
    return password_reset


@pytest.fixture
def mock_role() -> Mock:
    role = Mock(spec=Role)
    role.id = 1
    role.name = "test"
    role.description = "test"
    role.scopes = {"test"}
    role.created_at = datetime.now(UTC)
    role.updated_at = None
    return role


@pytest.fixture
def mock_permission() -> Mock:
    permission = Mock(spec=Permission)
    permission.id = 1
    permission.scope = "test"
    permission.title = "test"
    permission.description = "test"
    return permission


@pytest.fixture
def mock_team(mock_user: Mock) -> Mock:
    team = Mock(spec=Team)
    team.id = uuid4()
    team.owner_id = mock_user.id
    team.name = Faker().name()
    team.slug = Faker().slug()
    team.description = Faker().sentence()
    team.default = False
    team.created_at = datetime.now(UTC)
    team.updated_at = None
    return team


@pytest.fixture
def mock_team_invitation(mock_team: Mock, mock_user: Mock) -> Mock:
    team_invitation = Mock(spec=TeamInvitation)
    team_invitation.id = uuid4()
    team_invitation.team_id = mock_team.id
    team_invitation.inviter_id = mock_user.id
    team_invitation.email = Faker().email()
    team_invitation.role = "Member"
    team_invitation.token = uuid4().hex
    team_invitation.created_at = datetime.now(UTC)
    return team_invitation


@pytest.fixture
def mock_device() -> Mock:
    mock_device = Mock(spec=Device)
    mock_device.id = uuid4()
    mock_device.name = "device"
    mock_device.description = "description"
    mock_device.device_type = DeviceType.DEVICE
    mock_device.token = uuid4().hex
    mock_device.status = DeviceStatus.OFFLINE
    mock_device.image_url = "image_url"
    mock_device.disabled = False
    mock_device.last_connection = None
    mock_device.meta_data = {}
    mock_device.team_id = uuid4()
    mock_device.created_at = datetime.now()
    mock_device.updated_at = None
    return mock_device


@pytest.fixture
def mock_connect_log() -> Mock:
    mock = Mock(spec=ConnectLog)
    mock.device_id = uuid4()
    mock.ts = datetime.now()
    mock.ip = "192.168.1.200"
    mock.connect_status = 0
    mock.keep_alive = 60
    return mock
