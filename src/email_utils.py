"""Utility module for sending emails with optional image attachments."""
import os
import ssl
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import _ssl
from dotenv import load_dotenv

# Adding environment variables
load_dotenv()
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
RECEIVER = os.getenv("RECEIVER")

def send_email(subject: str, body: str, image_stream=None):
    """
    Send an email with an optional image attachment.
    
    Args:
        subject (str): The subject of the email.
        body (str): The body content of the email.
        image_stream (BytesIO, optional): A BytesIO stream containing the image data.
        
    Raises:
        smtplib.SMTPException: If there's an error sending the email.
    """
    try:
        # Create message
        msg = MIMEMultipart()
        msg["From"] = EMAIL
        msg["To"] = RECEIVER
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))
        
        # Attach image if available
        if image_stream:
            image = MIMEImage(image_stream.getvalue())
            image.add_header("Content-Disposition", "attachment", filename="image.png")
            msg.attach(image)

        # Create SSL context with legacy renegotiation support
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.options |= 0x4  # Enable legacy renegotiation (SSL_OP_LEGACY_SERVER_CONNECT)
        context.options &= ~ssl.OP_NO_TLSv1  # Enable TLSv1
        context.options &= ~ssl.OP_NO_TLSv1_1  # Enable TLSv1.1
        context.options &= ~ssl.OP_NO_SSLv3  # Enable SSLv3
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        
        # Set up supported ciphers
        context.set_ciphers('DEFAULT@SECLEVEL=1')

        # Connect using SMTP_SSL with port 465
        with smtplib.SMTP_SSL("mail.kurumsaleposta.com", 465, context=context) as server:
            server.login(EMAIL, PASSWORD)
            server.send_message(msg)
            
    except smtplib.SMTPException as e:
        print(f"SMTP Error: {str(e)}")
        raise
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise