
from notifications.email import send_email_notification

send_email_notification(
    pod_name="email-test-pod",
    issue="EmailTest",
    namespace="default"
)