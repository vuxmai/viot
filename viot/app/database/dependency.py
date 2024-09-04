from collections.abc import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .context import session_ctx
from .engine import async_engine


async def get_session() -> AsyncGenerator[None, None]:
    """
    Provides a new session for database operations.
    This function acts as a FastAPI dependency, generating an asynchronous
    sequence of `AsyncSession` objects. It initializes a new session using
    `AsyncSessionFactory`, associates the session with the `CrudRepository`
    context, and yields the session for use. After the session is utilized,
    it commits any changes and closes the session.

    **Important Notes:**
    - This function is designed to be used as a dependency within FastAPI
    routes and services, not directly.
    - **Compatibility:** This function is created for use with FastAPI
    version > 0.106. If using a lower version, manual commit is required
    after database operations.
    - In FastAPI versions > 0.106, any code following the `yield` statement
    will execute before the result is returned to the client.

    **Example Usage in a FastAPI Route:**
    ```python
    async def my_route(session: AsyncSession = Depends(get_session)):
        # Utilize the session for database operations
        pass
    ```
    """
    async with AsyncSession(async_engine, expire_on_commit=False, autoflush=False) as session:
        token = session_ctx.set(session)
        try:
            async with session.begin():
                yield
        finally:
            session_ctx.reset(token)


DependSession = Depends(get_session)
