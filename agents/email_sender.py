"""
Email Sender Agent.

Sends the generated HTML newsletter
to configured email recipients.
"""

from __future__ import annotations

import os
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv

from config.settings import (
    EMAIL_SMTP_SERVER,
    EMAIL_SMTP_PORT,
    EMAIL_SUBJECT,
)

from utils.logger import get_logger

load_dotenv()

logger = get_logger(__name__)

class EmailSender:
    """
    Sends newsletters via SMTP.
    """
    
    def __init__(self) -> None:
        
        self.sender_email = os.getenv(
            "EMAIL_ADDRESS"
        )
        
        self.app_password = os.getenv(
            "EMAIL_APP_PASSWORD"
        )
        
        recipients = os.getenv(
            "EMAIL_RECIPIENTS",
            "",
        )
        
        self.recipients = [
            email.strip()
            for email in recipients.split(",")
            if email.strip()
        ]
    
    def send(
        self,
        html_content: str,
    ) -> bool:
        """
        Send the HTML newsletter.
        
        Args:
            html_content:
                Newsletter HTML.
                
        Returns:
            True if successul,
            otherwise False.
        """
        
        logger.info(
            "Starting Email Sender..."
        )
        
        if not self.sender_email:
            
            raise ValueError(
                "Email Address not configured"
            )
            
        if not self.app_password:
            
            raise ValueError(
                "Email App Password not configured"
            )
            
        if not self.recipients:
            
            raise ValueError(
                "Email Recipients not configured"
            )
            
        message = MIMEMultipart("alternative")
        
        message["Subject"] = EMAIL_SUBJECT
        message["From"] = self.sender_email
        message["To"] = ", ".join(self.recipients)
        
        html_part = MIMEText(
            html_content,
            "html",
            "utf-8",
        )
        
        message.attach(
            html_part,
        )
        
        
        try:

            logger.info(
                "Connecting to SMTP server..."
            )
            
            with smtplib.SMTP(
                EMAIL_SMTP_SERVER,
                EMAIL_SMTP_PORT,
                timeout=30,
            ) as smtp:
                
                smtp.starttls()
                
                smtp.login(
                    self.sender_email,
                    self.app_password,
                )
                
                smtp.sendmail(
                    self.sender_email,
                    self.recipients,
                    message.as_string(),
                )
            
            logger.info(
                "Email sent successfully."
            )
            
            logger.info(
                "Recipients: %s",
                ", ".join(
                    self.recipients
                ),
            )
            
            return True
        
        except Exception as exc:
            
            logger.exception(
                "Email Sending failed %s", 
                exc,
            )
            
            return False
        

email_sender = EmailSender()

def email_sender_node(
    state,
):
    """
    LangGraph node responsible for 
    sending the newsletter email.
    """
    
    logger.info(
        "Starting Email Sender Node..."
    )
    
    success = email_sender.send(
        state["html_content"]
    )
    
    if success:
        
        logger.info(
            "Email Sender completed successfully."
        )
        
    else:
        
        logger.error(
            "Email Sender failed."
        )
        
    return { 
        "email_sent": success,}
                
        
        
        