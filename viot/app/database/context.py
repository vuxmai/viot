from contextvars import ContextVar

from sqlalchemy.ext.asyncio import AsyncSession

session_ctx = ContextVar[AsyncSession]("session")
