from flask import current_app
from flask_mail import Message

from app.core.extensions import mail

class EmailService:

    #Shared email service for the app

    @staticmethod
    def send_email(
            subject,
            recipients,
            body=None,
            html=None,
            sender=None,
            reply_to=None
    ):
        
        if not recipients:
            raise ValueError("At least on recipient is required.")
        
        if isinstance(recipients, str):
            recipients = [recipients]

        message = Message(
            subject=subject,
            recipients=recipients,
            body=body,
            html=html,
            sender=sender or current_app.config.get(
                'MAIL_DEFAULT_SENDER'
        ), reply_to=reply_to
            )
        
        mail.send(message)

        return True
    
    @staticmethod
    def send_enquiry_notification(cls, enquiry):

        recipient = current_app.config.get(
            "ENQUIRY_NOTIICATION_EMAIL"
        )

        if not recipient:
            raise RuntimeError(
                "ENQUIRY_NOTIFICATION_EMAIL is not configured."
            )
        
        subject = (
            f"New website enquiry from {enquiry.name}"
        )

        body = f"""

New website enquiry recieved.

Name : {enquiry.name}
Email : {enquiry.email}
Phone : {enquiry.phone}

Subject : {enquiry.subject}

Message :

{enquiry.message}

Received : 
{enquiry.created_at}


""".strip()
        
        return cls.send_mail(
            subject=subject,
            recipient=recipient,
            body=body,
            reply_to=enquiry.email
        )
    
    