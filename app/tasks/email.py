import asyncio
from fastapi_mail import FastMail, MessageSchema
from app.config import mail_config
from app.celery_app import celery_app


@celery_app.task(name="app.tasks.email.send_reset_email")
def send_reset_email(to_email: str, reset_link: str):
    message = MessageSchema(
        subject="reset password", 
        recipients=[to_email],
        body=f"""
        <p>Greetings!</p>
        <p>to reset password, please click on the button:</p>
        <a href="{reset_link}" style="
            display: inline-block;
            padding: 12px 24px;
            background-color: #4CAF50;
            color: white;
            text-decoration: none;
            border-radius: 6px;
            font-weight: bold;">
            Reset Password
        </a>
        <p>If you did not request a password reset, ignore this letter.</p>
    """,
        subtype="html"
    )
    asyncio.run(FastMail(mail_config).send_message(message)) 
    return {"message": "Password reset link sent to your email."}