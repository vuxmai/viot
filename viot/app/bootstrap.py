from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.common.exception.handler import register_exception_handlers
from app.common.fastapi import JSONResponse, setup_openapi
from app.config import settings
from app.container import injector
from app.extension.redis.client import RedisClient

from . import __version__


@asynccontextmanager
async def _lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    redis_client = injector.get(RedisClient)
    await redis_client.open()

    yield

    await redis_client.close()


def create_app() -> FastAPI:
    app = FastAPI(
        **settings.FASTAPI_CONFIG,
        default_response_class=JSONResponse,
        lifespan=_lifespan,
    )

    setup_modules()  # Make sure setup_modules call before import routes

    register_middleware(app)

    setup_openapi(app)

    register_router(app)

    register_exception_handlers(app)

    return app


def setup_modules() -> None:
    """
    Setup modules for the application.
    Using `injector` to install modules.
    """
    from app.celery_worker.module import CeleryWorkerModule
    from app.database.module import DatabaseModule
    from app.extension.redis.module import RedisModule
    from app.module.auth.module import AuthModule
    from app.module.email.module import EmailModule
    from app.module.team.module import TeamModule
    from app.module.team_invitation.module import TeamInvitationModule
    from app.module.user.module import UserModule

    injector.binder.install(DatabaseModule)
    injector.binder.install(RedisModule)
    injector.binder.install(CeleryWorkerModule)
    injector.binder.install(EmailModule)

    injector.binder.install(UserModule)
    injector.binder.install(AuthModule)
    injector.binder.install(TeamModule)
    injector.binder.install(TeamInvitationModule)


def register_middleware(app: FastAPI) -> None:
    # CORS needs to be added last

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOW_CORS_ORIGINS,  # type: ignore
        allow_credentials=settings.ALLOW_CREDENTIALS,
        allow_methods=settings.ALLOW_METHODS,
        allow_headers=settings.ALLOW_CORS_HEADERS,
    )


def register_router(app: FastAPI) -> None:
    from app.routes import router as api_router

    @app.get("/health", include_in_schema=False)
    async def health():  # type: ignore
        return {
            "status": "ok",
            "version": __version__,
        }

    app.include_router(api_router, prefix=settings.API_PREFIX)
