from app.extension.email.enums import TemplateType
from app.extension.email.utils import get_template, render, send

from ..celery import celery_app
from .enums import EmailTaskType


@celery_app.task(name=EmailTaskType.VERIFY_ACCOUNT)
def send_verify_account_email(email: str, name: str, verify_url: str) -> None:
    template = get_template(TemplateType.VERIFY_ACCOUNT)
    html_content = render(template=template, ctx={"name": name, "url": verify_url})
    send(to=email, subject="Verify your account", html_content=html_content)


@celery_app.task(name=EmailTaskType.RESET_PASSWORD)
def send_reset_password_email(email: str, name: str, ui_link: str) -> None:
    template = get_template(TemplateType.RESET_PASSWORD)
    html_content = render(template=template, ctx={"name": name, "link": ui_link})
    send(to=email, subject="Reset your password", html_content=html_content)


@celery_app.task(name=EmailTaskType.TEAM_INVITATION)
def send_team_invitation_email(
    email: str, name: str, invitor_name: str, team_name: str, ui_link: str
) -> None:
    template = get_template(TemplateType.TEAM_INVITATION)
    html_content = render(
        template=template,
        ctx={
            "name": name,
            "invitor_name": invitor_name,
            "team_name": team_name,
            "link": ui_link,
        },
    )
    send(to=email, subject="You are invited to a team", html_content=html_content)
