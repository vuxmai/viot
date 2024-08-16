from injector import Binder, Module, SingletonScope

from .service import EmailService, IEmailService


class EmailModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(IEmailService, EmailService, SingletonScope)  # type: ignore
