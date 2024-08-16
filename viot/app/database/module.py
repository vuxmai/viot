from contextvars import ContextVar

from injector import Module, provider
from sqlalchemy.ext.asyncio import AsyncSession

from .context import session_ctx


class DatabaseModule(Module):
    # def configure(self, binder: Binder) -> None:
    # binder.bind(ContextVar[AsyncSession], session_ctx, SingletonScope)
    # Error: raise UnknownProvider('couldn\'t determine provider for %r to %r' % (interface, to))
    # Use @provider to bind the context variable
    @provider
    def provide_session_context(self) -> ContextVar[AsyncSession]:
        return session_ctx
