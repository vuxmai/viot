from typing import Annotated

from classy_fastapi import get, post
from fastapi import Body, Cookie, Query, Response
from fastapi.responses import RedirectResponse
from injector import inject

from app.common.controller import Controller
from app.common.fastapi.serializer import JSONResponse
from app.config import app_settings
from app.database.dependency import DependSession

from ..dependency import DependCurrentUser
from ..dto.auth_dto import LoginDto, RegisterDto, TokenDto
from ..dto.reset_password_dto import ForgotPasswordDto, ResetPasswordDto
from ..dto.user_dto import UserDto
from ..model.user import User
from ..service.auth_service import AuthService
from ..service.password_reset_service import PasswordResetService
from ..service.token_service import TokenService


class AuthController(Controller):
    @inject
    def __init__(
        self,
        auth_service: AuthService,
        token_service: TokenService,
        password_reset_service: PasswordResetService,
    ) -> None:
        super().__init__(prefix="/auth", tags=["Auth"], dependencies=[DependSession])
        self._auth_service = auth_service
        self._token_service = token_service
        self._password_reset_service = password_reset_service

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
        response.set_cookie(**self._token_service.get_refresh_token_settings(result.refresh_token))
        return response

    @post(
        "/register",
        summary="Register a new user",
        status_code=201,
        responses={201: {"model": UserDto}},
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
        await self._auth_service.verify_account(token=token)
        return RedirectResponse(url=f"{app_settings.UI_URL}/login")

    @post("/logout", summary="Logout the current user", status_code=204)
    async def logout(
        self,
        *,
        user: Annotated[User, DependCurrentUser],
        refresh_token: Annotated[str, Cookie(..., alias="refreshToken")],
        response: Response,
    ) -> JSONResponse[None]:
        """Logout the current user"""
        await self._auth_service.logout(refresh_token=refresh_token)
        response.delete_cookie(key="refreshToken")
        return JSONResponse.no_content()

    @post(
        "/refresh",
        summary="Refresh access token",
        status_code=200,
        responses={200: {"model": TokenDto}},
    )
    async def refresh(
        self, *, refresh_token: Annotated[str, Cookie(..., alias="refreshToken")]
    ) -> JSONResponse[TokenDto]:
        """Refresh access token"""
        result = await self._token_service.renew_token(refresh_token=refresh_token)
        response = JSONResponse(content=result, status_code=200)
        response.set_cookie(**self._token_service.get_refresh_token_settings(result.refresh_token))
        return response

    @post("/forgot-password", summary="Forgot password", status_code=204)
    async def forgot_password(
        self, *, forgot_password_dto: Annotated[ForgotPasswordDto, Body(...)]
    ) -> JSONResponse[None]:
        """Forgot password"""
        await self._password_reset_service.forgot_password(email=forgot_password_dto.email)
        return JSONResponse.no_content()

    @post("/reset-password", summary="Reset password", status_code=204)
    async def reset_password(
        self, *, reset_password_dto: Annotated[ResetPasswordDto, Body(...)]
    ) -> JSONResponse[None]:
        """Reset password"""
        await self._password_reset_service.reset_password(reset_password_dto=reset_password_dto)
        return JSONResponse.no_content()
