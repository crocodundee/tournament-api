from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from fastapi import BackgroundTasks

import os

from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from jinja2 import Environment, FileSystemLoader, select_autoescape

from config.base import (
    DEFAULT_FROM_EMAIL,
    SMTP_HOST,
    SMTP_PASSWORD,
    SMTP_PORT,
    SMTP_USER,
)


def render_template(template_name: str, params: dict) -> str:
    """
    Render a Jinja2 template with the given parameters.
    Args:
        template_name: Filename of the template (relative to 'templates' directory).
        params: Dictionary of parameters to render in the template.
    Returns:
        Rendered template as a string.
    """
    templates_dir = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "templates"
    )
    env = Environment(
        loader=FileSystemLoader(templates_dir),
        autoescape=select_autoescape(["html", "xml"]),
    )
    template = env.get_template(template_name)
    return template.render(**params)


conf = ConnectionConfig(
    MAIL_USERNAME=SMTP_USER,
    MAIL_PASSWORD=SMTP_PASSWORD,
    MAIL_FROM=DEFAULT_FROM_EMAIL,
    MAIL_PORT=SMTP_PORT,
    MAIL_SERVER=SMTP_HOST,
    MAIL_STARTTLS=True if SMTP_USER and SMTP_PASSWORD else False,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True if SMTP_USER and SMTP_PASSWORD else False,
)


def send_email(
    subject: str,
    recipients: List[str],
    background_tasks: "BackgroundTasks",
    body: str = "",
    files: List[str] = [],
    message_type: MessageType = MessageType.html,
):
    """
    Send an email using FastAPI-Mail. Can be used in FastAPI background tasks.
    Args:
        subject: Email subject
        recipients: List of recipient emails
        body: Text body (for text emails)
        body_html: HTML body (for html emails)
        files: List of file paths to attach
        message_type: 'text', 'html', or 'file'
        background_tasks: FastAPI BackgroundTasks instance (optional)
    """
    message = MessageSchema(
        subject=subject,
        recipients=recipients,
        body=body,
        subtype=message_type,
        attachments=files,
    )
    fm = FastMail(conf)
    background_tasks.add_task(fm.send_message, message)
