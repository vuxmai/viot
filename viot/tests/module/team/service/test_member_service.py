from datetime import datetime
from unittest.mock import AsyncMock, Mock, patch
from uuid import uuid4

import pytest

from app.database.repository.pagination import Page
from app.module.auth.exception.role_exception import RoleIdNotFoundException
from app.module.auth.exception.user_exception import UserNotFoundException
from app.module.auth.repository.user_repository import TeamMember
from app.module.team.constants import TEAM_ROLE_OWNER
from app.module.team.dto.member_dto import MemberUpdateDto
from app.module.team.exception.member_exception import AssignSensitiveRoleException
from app.module.team.service.member_service import MemberService


@pytest.fixture
def mock_user_repository() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def mock_role_repository() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def mock_user_team_role_repository() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def member_service(
    mock_user_repository: AsyncMock,
    mock_role_repository: AsyncMock,
    mock_user_team_role_repository: AsyncMock,
) -> MemberService:
    return MemberService(
        user_repository=mock_user_repository,
        role_repository=mock_role_repository,
        user_team_role_repository=mock_user_team_role_repository,
    )


async def test_find_paging_members(
    member_service: MemberService, mock_user_repository: AsyncMock, mock_user: Mock
) -> None:
    # given
    items = [
        TeamMember(user=mock_user, role="Member", joined_at=datetime.now()),
        TeamMember(user=mock_user, role="Owner", joined_at=datetime.now()),
    ]
    mock_user_repository.find_paging_member_by_team_id.return_value = Page(
        items=items, total_items=20, page=0, page_size=20
    )

    # when
    result = await member_service.find_paging_members(
        page=0,
        page_size=20,
        sort_direction_joined_at="desc",
        team_id=uuid4(),
    )

    # then
    assert len(result.items) == 2
    assert result.items[0].id == mock_user.id
    assert result.total_items == 20
    assert result.page == 0
    assert result.page_size == 20


async def test__get_member_by_id_and_team_id(
    member_service: MemberService, mock_user_repository: AsyncMock, mock_user: Mock
) -> None:
    # given
    mock_user_repository.find_user_by_id_and_team_id.return_value = TeamMember(
        user=mock_user, role="Member", joined_at=datetime.now()
    )

    # when
    result = await member_service._get_member_by_id_and_team_id(  # type: ignore
        team_id=uuid4(),
        member_id=uuid4(),
    )

    # then
    assert result.user == mock_user
    assert result.role == "Member"


async def test__get_member_by_id_and_team_id_raise_user_not_found(
    member_service: MemberService, mock_user_repository: AsyncMock
) -> None:
    # given
    mock_user_repository.find_user_by_id_and_team_id.return_value = None

    # when
    with pytest.raises(UserNotFoundException):
        await member_service._get_member_by_id_and_team_id(  # type: ignore
            team_id=uuid4(),
            member_id=uuid4(),
        )


async def test_get_member_by_id_and_team_id(
    member_service: MemberService, mock_user_repository: AsyncMock, mock_user: Mock
) -> None:
    # given
    mock_user_repository.find_user_by_id_and_team_id.return_value = TeamMember(
        user=mock_user, role="Member", joined_at=datetime.now()
    )

    # when
    result = await member_service.get_member_by_id_and_team_id(
        team_id=uuid4(),
        member_id=uuid4(),
    )

    # then
    assert result.id == mock_user.id
    assert result.role == "Member"


async def test_update_member(
    member_service: MemberService, mock_role_repository: AsyncMock, mock_user: Mock
) -> None:
    # given
    team_id = uuid4()
    member_id = uuid4()
    role_id = 1
    role_name = "Member"

    mock_role_repository.find_role_name_by_role_id_and_team_id.return_value = role_name

    # when
    with patch.object(MemberService, "_get_member_by_id_and_team_id") as mock_get_member:
        mock_get_member.return_value = TeamMember(
            user=mock_user, role="Another role", joined_at=datetime.now()
        )
        result = await member_service.update_member(
            team_id=team_id,
            member_id=member_id,
            member_update_dto=MemberUpdateDto(role_id=role_id),
        )

    # then
    assert result.id == mock_user.id
    assert result.role == role_name


async def test_update_member_no_role_id(member_service: MemberService, mock_user: Mock) -> None:
    # given
    team_id = uuid4()
    member_id = uuid4()

    # when
    with patch.object(MemberService, "_get_member_by_id_and_team_id") as mock_get_member:
        mock_get_member.return_value = TeamMember(
            user=mock_user, role="Another role", joined_at=datetime.now()
        )
        result = await member_service.update_member(
            team_id=team_id,
            member_id=member_id,
            member_update_dto=MemberUpdateDto(role_id=None),
        )

    # then
    assert result.id == mock_user.id
    assert result.role == "Another role"


async def test_update_member_raise_role_id_not_found(
    member_service: MemberService, mock_role_repository: AsyncMock
) -> None:
    # given
    team_id = uuid4()
    member_id = uuid4()
    role_id = 1

    mock_role_repository.find_role_name_by_role_id_and_team_id.return_value = None

    # when
    with pytest.raises(RoleIdNotFoundException):
        await member_service.update_member(
            team_id=team_id,
            member_id=member_id,
            member_update_dto=MemberUpdateDto(role_id=role_id),
        )


async def test_update_member_same_role(
    member_service: MemberService,
    mock_role_repository: AsyncMock,
    mock_user_team_role_repository: AsyncMock,
    mock_user: Mock,
) -> None:
    # given
    team_id = uuid4()
    member_id = uuid4()
    role_id = 1
    role_name = "Member"

    mock_role_repository.find_role_name_by_role_id_and_team_id.return_value = role_name

    # when
    with patch.object(MemberService, "_get_member_by_id_and_team_id") as mock_get_member:
        mock_get_member.return_value = TeamMember(
            user=mock_user, role=role_name, joined_at=datetime.now()
        )
        result = await member_service.update_member(
            team_id=team_id,
            member_id=member_id,
            member_update_dto=MemberUpdateDto(role_id=role_id),
        )

    # then
    assert result.id == mock_user.id
    assert result.role == role_name


async def test_delete_member(
    member_service: MemberService, mock_user_repository: AsyncMock
) -> None:
    # given
    team_id = uuid4()
    member_id = uuid4()

    # when
    await member_service.delete_member(team_id=team_id, member_id=member_id)

    # then
    mock_user_repository.delete_user_by_id_and_team_id.assert_called_once()


async def test_validate_sensitive_role(
    member_service: MemberService,
) -> None:
    # given
    role_name = "Member"

    # when
    member_service.validate_sensitive_role(role_name=role_name)


async def test_validate_sensitive_role_raise_assign_role_sensitive(
    member_service: MemberService,
) -> None:
    # given
    role_name = TEAM_ROLE_OWNER

    # when
    with pytest.raises(AssignSensitiveRoleException):
        member_service.validate_sensitive_role(role_name=role_name)
