from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import logging
from app import settings

logger = logging.getLogger(__name__)

# Email configuration
EMAIL_HOST = settings.email_host  # Using Mailtrap SMTP server
EMAIL_PORT = settings.email_port
EMAIL_HOST_USER = settings.email_host_user
EMAIL_HOST_PASSWORD = settings.email_host_password

# Check if email credentials are set
if not EMAIL_HOST_USER or not EMAIL_HOST_PASSWORD:
    logger.error("Email credentials are not set. Please check your environment variables.")

def send_email(subject: str, body: str, recipients: list):
    """
    Function to send an email with the provided subject and body to the specified recipients.
    """
    # Check if email credentials are set
    if not EMAIL_HOST_USER or not EMAIL_HOST_PASSWORD:
        logger.error("Email credentials are not set. Cannot send email.")
        return

    # Create the email message
    msg = MIMEMultipart('alternative')
    msg["Subject"] = subject
    msg["From"] = EMAIL_HOST_USER
    msg["To"] = ", ".join(recipients)

    # Attach the HTML content
    html_content = body
    msg.attach(MIMEText(html_content, 'html'))

    # Send the email
    try:
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
        server.sendmail(EMAIL_HOST_USER, recipients, msg.as_string())
        server.quit()
        logger.info("Email sent successfully.")
    except Exception as e:
        logger.error("Failed to send email", exc_info=True)
