from flask_mail import Message
from gemlibapp import mail
from gemlibapp.config import Config


def send_reminder_email(user_email, subject, message):
    msg = Message(subject=subject, sender=Config.MAIL_USERNAME, recipients=[user_email])
    msg.body = message
    mail.send(msg)


class DefaultReminderMessage():
    default_message = """Liebe Heilige,
    das von dir ausgeliehen Buch ist diese Woche am Tag des Herrn fällig.
    Bitte vergisst du nicht, es zurückzusenden.
    Vielen Dank.

    Grüße,
    Bücher dienende Heilige 
    --------------
    Hello Saint,
    The book you have borrowed is due this week on Lord's Day.
    Please do not forget to return it.
    Thank you.

    Regards,
    Saints serving with books
    """

    default_subject = "Das Buch ist bald fällig. The book is due soon."

