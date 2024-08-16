from collections.abc import AsyncGenerator

from fastapi import BackgroundTasks, Depends, Request

from .context import background_tasks_ctx, request_ctx


async def get_request(request: Request) -> AsyncGenerator[None, None]:
    token = request_ctx.set(request)
    yield
    request_ctx.reset(token)


async def get_background_tasks(background_tasks: BackgroundTasks) -> AsyncGenerator[None, None]:
    token = background_tasks_ctx.set(background_tasks)
    yield
    background_tasks_ctx.reset(token)


DependRequest = Depends(get_request)
DependBackgroundTasks = Depends(get_background_tasks)
