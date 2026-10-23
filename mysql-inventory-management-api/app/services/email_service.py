import logging
import smtplib
from email.message import EmailMessage

from app.core.config import settings

logger = logging.getLogger(__name__)


def send_email(
    recipient: str,
    subject: str,
    body: str,
) -> bool:
    """Send an email using configured SMTP settings."""
    if not all(
        [
            settings.SMTP_HOST,
            settings.SMTP_PORT,
            settings.SMTP_USERNAME,
            settings.SMTP_PASSWORD,
            settings.SMTP_SENDER_EMAIL,
        ]
    ):
        logger.warning("Email not sent: SMTP settings are incomplete.")
        return False

    message = EmailMessage()
    message["From"] = settings.SMTP_SENDER_EMAIL
    message["To"] = recipient
    message["Subject"] = subject
    message.set_content(body)

    try:
        with smtplib.SMTP(
            settings.SMTP_HOST,
            settings.SMTP_PORT,
            timeout=10,
        ) as smtp:
            smtp.starttls()
            smtp.login(
                settings.SMTP_USERNAME,
                settings.SMTP_PASSWORD,
            )
            smtp.send_message(message)

        logger.info("Email sent successfully.")
        return True

    except (OSError, smtplib.SMTPException):
        logger.exception("Failed to send email.")
        return False


def send_low_stock_alert(
    product_name: str,
    sku: str,
    quantity: int,
    reorder_level: int,
) -> bool:
    """Send a low-stock notification to the administrator."""
    if not settings.ADMIN_EMAIL:
        logger.warning("Low-stock alert not sent: ADMIN_EMAIL is missing.")
        return False

    subject = f"Low-stock alert: {product_name}"
    body = (
        "A product has reached its reorder threshold.\n\n"
        f"Product: {product_name}\n"
        f"SKU: {sku}\n"
        f"Current quantity: {quantity}\n"
        f"Reorder level: {reorder_level}\n"
    )

    return send_email(settings.ADMIN_EMAIL, subject, body)
