from datetime import UTC, datetime
from unittest.mock import Mock
from uuid import uuid4

import pytest
from faker import Faker

from app.module.auth.model import PasswordReset
from app.module.auth.utils import hash_password
from app.module.team.constant import TeamRole
from app.module.team.model import Team
from app.module.team_invitation.model import TeamInvitation
from app.module.user.constant import ViotUserRole
from app.module.user.model import User


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
    user.created_at = datetime.now()
    user.updated_at = None
    user.verified = True
    return user


@pytest.fixture
def mock_password_reset(mock_user: Mock) -> Mock:
    password_reset = Mock(spec=PasswordReset)
    password_reset.email = mock_user.email
    password_reset.token = uuid4().hex
    password_reset.created_at = datetime.now(UTC)
    return password_reset


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
    team_invitation.role = TeamRole.MEMBER
    team_invitation.token = uuid4().hex
    team_invitation.created_at = datetime.now(UTC)
    return team_invitation
