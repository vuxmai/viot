from app.module.email.service import IEmailService


class MockEmailService(IEmailService):
    def send_verify_account_email(self, *, email: str, name: str, verify_url: str) -> None:
        pass

    def send_reset_password_email(self, *, email: str, name: str, link: str) -> None:
        pass

    def send_team_invitation_email(
        self, *, email: str, name: str, invitor_name: str, team_name: str, link: str
    ) -> None:
        pass
