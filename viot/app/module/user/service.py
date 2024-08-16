import logging
from uuid import UUID

from injector import inject

from app.module.auth.utils import hash_password, verify_password

from .dto import ChangePasswordDto, UserDto, UserUpdateDto
from .exception import PasswordNotMatchException, UserNotFoundException
from .repository import UserRepository

logger = logging.getLogger(__name__)


class UserService:
    @inject
    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository

    async def change_password(
        self, *, user_id: UUID, change_password_dto: ChangePasswordDto
    ) -> None:
        user = await self._user_repository.find(id=user_id)
        if not user:
            raise UserNotFoundException
        if not verify_password(change_password_dto.old_password, user.password):
            raise PasswordNotMatchException

        await self._user_repository.update_password(
            user_id, hash_password(change_password_dto.new_password)
        )

    async def update_user(self, *, user_id: UUID, user_update_dto: UserUpdateDto) -> UserDto:
        user = await self._user_repository.find(user_id)
        if not user:
            raise UserNotFoundException

        for k, v in user_update_dto.model_dump(exclude_none=True).items():
            setattr(user, k, v)

        user = await self._user_repository.save(user)
        return UserDto.model_validate(user)

    async def delete_user(self, *, user_id: UUID) -> None:
        user = await self._user_repository.find(user_id)
        if not user:
            raise UserNotFoundException

        await self._user_repository.delete(user)
