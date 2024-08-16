from typing import Annotated

from classy_fastapi import get, post
from fastapi import Body, Cookie, Query, Response
from fastapi.responses import RedirectResponse
from injector import inject

from app.common.controller import Controller
from app.common.fastapi.dependency import DependRequest
from app.common.fastapi.serializer import JSONResponse
from app.config import settings
from app.database.dependency import DependSession
from app.module.user.dto import UserDto
from app.module.user.model import User

from .dependency import DependCurrentUser
from .dto import ForgotPasswordDto, LoginDto, RegisterDto, ResetPasswordDto, TokenDto
from .service import AuthService
from .token import get_refresh_token_settings


class AuthController(Controller):
    @inject
    def __init__(self, auth_service: AuthService) -> None:
        super().__init__(prefix="/auth", tags=["Auth"], dependencies=[DependSession])
        self._auth_service = auth_service

    @post(
        "/login",
        summary="Authenticate a user",
        status_code=200,
        responses={200: {"model": TokenDto}},
    )
    async def login(self, *, login_dto: Annotated[LoginDto, Body(...)]) -> JSONResponse[TokenDto]:
        """Authenticate a user"""
        result = await self._auth_service.login(login_dto=login_dto)
        response = JSONResponse(content=result, status_code=200)
        response.set_cookie(**get_refresh_token_settings(result.refresh_token))
        return response

    @post(
        "/register",
        summary="Register a new user",
        status_code=201,
        responses={201: {"model": UserDto}},
        dependencies=[DependRequest],
    )
    async def register(self, *, register_dto: RegisterDto) -> JSONResponse[UserDto]:
        """Register a new user"""
        return JSONResponse(
            content=await self._auth_service.register(register_dto=register_dto),
            status_code=201,
        )

    @get("/verify-email", summary="Verify email", status_code=307, include_in_schema=False)
    async def verify_email(
        self, *, token: Annotated[str, Query(..., alias="token")]
    ) -> RedirectResponse:
        """Verify email"""
        await self._auth_service.verify_email(token=token)
        return RedirectResponse(url=f"{settings.UI_URL}/login")

    @post("/logout", summary="Logout the current user", status_code=204)
    async def logout(
        self,
        *,
        user: Annotated[User, DependCurrentUser],
        refresh_token: Annotated[str, Cookie(..., alias="refreshToken")],
        response: Response,
    ) -> JSONResponse[None]:
        """Logout the current user"""
        await self._auth_service.logout(user_id=user.id, refresh_token=refresh_token)
        response.delete_cookie(key="refreshToken")
        return JSONResponse.no_content()

    @post(
        "/refresh",
        summary="Refresh access token",
        status_code=200,
        responses={200: {"model": TokenDto}},
        dependencies=[DependCurrentUser],
    )
    async def refresh(
        self, *, refresh_token: Annotated[str, Cookie(..., alias="refreshToken")]
    ) -> JSONResponse[TokenDto]:
        """Refresh access token"""
        result = await self._auth_service.renew_token(refresh_token=refresh_token)
        response = JSONResponse(content=result, status_code=200)
        response.set_cookie(**get_refresh_token_settings(result.refresh_token))
        return response

    @post("/forgot-password", summary="Forgot password", status_code=204)
    async def forgot_password(
        self, *, forgot_password_dto: Annotated[ForgotPasswordDto, Body(...)]
    ) -> JSONResponse[None]:
        """Forgot password"""
        await self._auth_service.forgot_password(email=forgot_password_dto.email)
        return JSONResponse.no_content()

    @post("/reset-password", summary="Reset password", status_code=204)
    async def reset_password(
        self, *, reset_password_dto: Annotated[ResetPasswordDto, Body(...)]
    ) -> JSONResponse[None]:
        """Reset password"""
        await self._auth_service.reset_password(reset_password_dto=reset_password_dto)
        return JSONResponse.no_content()
