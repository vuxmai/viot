from abc import ABC, abstractmethod
from collections.abc import Iterable, Sequence
from contextvars import ContextVar
from typing import Any, Generic, TypeVar, get_args

from injector import inject
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.base import Base

TModel = TypeVar("TModel")
TPrimaryKey = TypeVar("TPrimaryKey")
TBaseModel = TypeVar("TBaseModel", bound=Base)


class AsyncSqlalchemyRepository:
    @inject
    def __init__(self, session_ctx: ContextVar[AsyncSession]):
        self._session_ctx = session_ctx

    @property
    def session(self) -> AsyncSession:
        return self._session_ctx.get()


class ICrudRepository(Generic[TModel, TPrimaryKey], ABC):
    @abstractmethod
    async def find(self, id: TPrimaryKey) -> TModel | None:
        """Find a single object by its primary key."""

    @abstractmethod
    async def find_all(self) -> Iterable[TModel]:
        """Find all objects in the repository."""

    @abstractmethod
    async def save(self, obj: TModel) -> TModel:
        """Save an object to the repository."""

    @abstractmethod
    async def delete(self, obj: TModel) -> None:
        """Delete an object from the repository."""


class CrudRepository(AsyncSqlalchemyRepository, ICrudRepository[TBaseModel, TPrimaryKey]):
    """
    A repository that implements the CRUD operations.

    This repository is designed to be used with a SQLAlchemy ORM.

    To use this repository, you need to provide the model type and the primary key type.

    Example:
    ```python
    class UserRepository(CrudRepository[Product, int]):
        pass
    ```
    """

    def __new__(
        cls: type[Any], *args: Any, **kwargs: Any
    ) -> "CrudRepository[TBaseModel, TPrimaryKey]":
        if not hasattr(cls, "_model"):
            cls._model = get_args(cls.__orig_bases__[0])[0]
        return super().__new__(cls)  # type: ignore

    async def find(self, id: TPrimaryKey) -> TBaseModel | None:
        return await self.session.get(self._model, id, populate_existing=True)

    async def find_all(self) -> Sequence[TBaseModel]:
        return (await self.session.scalars(select(self._model))).all()

    async def save(self, obj: TBaseModel) -> TBaseModel:
        self.session.add(obj)
        await self.session.flush()
        return obj

    async def delete(self, obj: TBaseModel) -> None:
        await self.session.delete(obj)
        await self.session.flush()

    async def delete_by_id(self, id: TPrimaryKey) -> None:
        stmt = delete(self._model).where(self._model.id == id)
        await self.session.execute(stmt)
