from datetime import UTC, datetime
from email.message import EmailMessage
import smtplib

from app.config import Settings
from app.schemas import Lead


class EmailService:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def send_lead_emails(self, lead: Lead) -> None:
        self._send(
            to_email=lead.email,
            subject="We received your information",
            body=(
                f"Hi {lead.first_name},\n\n"
                "Thanks for submitting your information. Our team has received your resume "
                "and will reach out if there is a fit.\n\n"
                "Best,\nProspect Portal Team"
            ),
        )
        self._send(
            to_email=self.settings.attorney_email,
            subject=f"New lead submitted: {lead.first_name} {lead.last_name}",
            body=(
                "A new prospect submitted the lead form.\n\n"
                f"Name: {lead.first_name} {lead.last_name}\n"
                f"Email: {lead.email}\n"
                f"Resume: {lead.resume_filename}\n"
                f"Status: {lead.status.value}\n"
            ),
        )

    def _send(self, to_email: str, subject: str, body: str) -> None:
        if not self.settings.smtp_host:
            self._write_to_outbox(to_email, subject, body)
            return

        message = EmailMessage()
        message["From"] = self.settings.smtp_from_email
        message["To"] = to_email
        message["Subject"] = subject
        message.set_content(body)

        with smtplib.SMTP(self.settings.smtp_host, self.settings.smtp_port) as server:
            if self.settings.smtp_use_tls:
                server.starttls()
            if self.settings.smtp_username and self.settings.smtp_password:
                server.login(self.settings.smtp_username, self.settings.smtp_password)
            server.send_message(message)

    def _write_to_outbox(self, to_email: str, subject: str, body: str) -> None:
        outbox_dir = self.settings.storage_dir / "outbox"
        outbox_dir.mkdir(parents=True, exist_ok=True)
        outbox_file = outbox_dir / "emails.log"
        timestamp = datetime.now(UTC).isoformat()
        with outbox_file.open("a", encoding="utf-8") as file:
            file.write(
                "\n".join(
                    [
                        "---",
                        f"timestamp: {timestamp}",
                        f"to: {to_email}",
                        f"subject: {subject}",
                        "",
                        body,
                        "",
                    ]
                )
            )
