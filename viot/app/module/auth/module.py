from injector import Binder, Module, SingletonScope

from .controller import AuthController
from .repository import PasswordResetRepository, RefreshTokenRepository
from .service import AuthService


class AuthModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(RefreshTokenRepository, RefreshTokenRepository, SingletonScope)
        binder.bind(PasswordResetRepository, PasswordResetRepository, SingletonScope)
        binder.bind(AuthService, AuthService, SingletonScope)
        binder.bind(AuthController, AuthController, SingletonScope)
