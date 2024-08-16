from injector import Binder, Module, SingletonScope

from .controller import UserController
from .repository import UserRepository
from .service import UserService


class UserModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(UserRepository, UserRepository, SingletonScope)
        binder.bind(UserService, UserService, SingletonScope)
        binder.bind(UserController, UserController, SingletonScope)
