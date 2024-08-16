import logging
from pathlib import Path
from typing import Any

import yagmail  # type: ignore
from jinja2 import Environment, FileSystemLoader, Template, select_autoescape

from .config import email_settings
from .enums import TemplateType
from .exceptions import TemplateNotFoundException

logger = logging.getLogger(__name__)


_yagmail = yagmail.SMTP(
    host=email_settings.SMTP_HOST,
    port=email_settings.SMTP_PORT,
    smtp_starttls=email_settings.SMTP_TLS,
    smtp_ssl=email_settings.SMTP_SSL,
    user=email_settings.SMTP_USER,
    password=email_settings.SMTP_PASSWORD,
)
_template_dir = Path(__file__).parent / "templates" / "html"
_env = Environment(loader=FileSystemLoader(_template_dir), autoescape=select_autoescape(["html"]))


template_map: dict[TemplateType, str] = {
    TemplateType.VERIFY_ACCOUNT: "verify-account.html",
    TemplateType.RESET_PASSWORD: "reset-password.html",
    TemplateType.TEAM_INVITATION: "team-invite-member.html",
}


def get_template(message_type: TemplateType) -> Template:
    """Get the Jinja2 template for the given message type."""
    template_key = template_map.get(message_type, "")
    try:
        template = _env.get_template(template_key)
    except Exception:
        raise TemplateNotFoundException(f"Template not found for message type: {message_type}")
    return template


def render(*, template: Template, ctx: dict[str, Any]) -> str:
    logger.debug(f"Rendering email template with context: {ctx}")
    return template.render(**ctx)


def send(*, to: str, subject: str, html_content: str) -> None:
    _yagmail.send(to=to, subject=subject, contents=[html_content])  # type: ignore
    logger.info(f"Email sent to {to}")
