
import os
import smtplib
from email.message import EmailMessage


def send_email_notification(pod_name, issue, namespace="default"):
    host = os.getenv("SMTP_HOST")
    port = int(os.getenv("SMTP_PORT", "587"))
    username = os.getenv("SMTP_USERNAME")
    password = os.getenv("SMTP_PASSWORD")
    recipient = os.getenv("ALERT_EMAIL")

    if not all([host, username, password, recipient]):
        print("Email skipped: SMTP settings are incomplete.")
        return False

    message = EmailMessage()
    message["Subject"] = f"Kubernetes Alert: {issue}"
    message["From"] = username
    message["To"] = recipient

    message.set_content(
        f"KUBERNETES ALERT\n\n"
        f"Namespace: {namespace}\n"
        f"Pod: {pod_name}\n"
        f"Issue: {issue}\n"
    )

    try:
        with smtplib.SMTP(host, port, timeout=20) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(username, password)
            server.send_message(message)

        print(f"Email sent for Pod: {pod_name}")
        return True

    except (OSError, smtplib.SMTPException) as error:
        print(f"Email failed: {type(error).__name__}: {error}")
        return False


if __name__ == "__main__":
    send_email_notification(
        pod_name="email-test-pod",
        issue="EmailTest",
        namespace="default"
    )