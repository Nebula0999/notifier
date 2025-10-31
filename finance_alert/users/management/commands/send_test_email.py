from django.core.management.base import BaseCommand, CommandParser
from django.core.mail import send_mail
from django.conf import settings


class Command(BaseCommand):
    help = "Send a test email using current EMAIL_* settings"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("to", nargs="?", help="Recipient email address (defaults to EMAIL_HOST_USER or DEFAULT_FROM_EMAIL)")
        parser.add_argument("--subject", default="Finance Alert: Test Email", help="Email subject")
        parser.add_argument("--body", default="This is a test email from Finance Alert.", help="Email body")

    def handle(self, *args, **options):
        to = options.get("to")
        subject = options["subject"]
        body = options["body"]

        sender = getattr(settings, "DEFAULT_FROM_EMAIL", None) or getattr(settings, "EMAIL_HOST_USER", None)
        recipient = to or getattr(settings, "EMAIL_HOST_USER", None) or getattr(settings, "DEFAULT_FROM_EMAIL", None)

        if not sender:
            self.stderr.write(self.style.ERROR("DEFAULT_FROM_EMAIL or EMAIL_HOST_USER must be set in settings/environment"))
            return
        if not recipient:
            self.stderr.write(self.style.ERROR("Provide a recipient email or set EMAIL_HOST_USER/DEFAULT_FROM_EMAIL"))
            return

        self.stdout.write(f"Sending test email to {recipient} from {sender} using {settings.EMAIL_BACKEND}...")

        try:
            sent = send_mail(subject, body, sender, [recipient], fail_silently=False)
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Failed to send email: {e}"))
            return

        if sent:
            self.stdout.write(self.style.SUCCESS("Email sent successfully"))
        else:
            self.stderr.write(self.style.ERROR("send_mail returned 0 (email not sent)"))
