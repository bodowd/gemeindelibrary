from flask_mail import Message
from gemlibapp import mail, scheduler
from gemlibapp.config import Config
from gemlibapp.models import User, Reminder, BookList
from datetime import timedelta, datetime


def send_reminder_email(user_email, subject, message):
    msg = Message(subject=subject, sender=Config.MAIL_USERNAME, recipients=[user_email])
    msg.body = message
    mail.send(msg)


# scheduler.add_job(func=daily_check, trigger="interval", days=1)


