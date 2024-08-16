from abc import ABC, abstractmethod

from celery import Celery
from injector import inject

from app.celery_worker.tasks.enums import EmailTaskType


class IEmailService(ABC):
    @abstractmethod
    def send_verify_account_email(self, *, email: str, name: str, verify_url: str) -> None:
        pass

    @abstractmethod
    def send_reset_password_email(self, *, email: str, name: str, link: str) -> None:
        pass

    @abstractmethod
    def send_team_invitation_email(
        self, *, email: str, name: str, invitor_name: str, team_name: str, link: str
    ) -> None:
        pass


class EmailService(IEmailService):
    @inject
    def __init__(self, celery_app: Celery) -> None:
        self._celery_app = celery_app

    def send_verify_account_email(self, *, email: str, name: str, verify_url: str) -> None:
        """Send an email to verify the user's account"""
        self._celery_app.send_task(
            EmailTaskType.VERIFY_ACCOUNT,
            kwargs={"email": email, "name": name, "verify_url": verify_url},
        )

    def send_reset_password_email(self, *, email: str, name: str, link: str) -> None:
        """Send an email to reset the user's password"""
        self._celery_app.send_task(
            EmailTaskType.RESET_PASSWORD,
            kwargs={"email": email, "name": name, "link": link},
        )

    def send_team_invitation_email(
        self, *, email: str, name: str, invitor_name: str, team_name: str, link: str
    ) -> None:
        """Send an email to invite a user to a team"""
        self._celery_app.send_task(
            EmailTaskType.TEAM_INVITATION,
            kwargs={
                "email": email,
                "name": name,
                "invitor_name": invitor_name,
                "team_name": team_name,
                "link": link,
            },
        )
