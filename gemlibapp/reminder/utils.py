from flask_mail import Message
from gemlibapp import mail


def send_reminder_email(user):
    msg = Message(subject='Das Buch ist bald fällig! The book is due soon! ', sender='gemeindelibrary@gmail.com', recipients=[user.email])
    # _external=True gives an absolute url rather than a relative url. Gives full domain
    msg.body = f'''Liebe Heilige, das Buch, das du ausgescheckt hast, ist fällig. 

Bitte vergisst du nicht, es zurückzusenden!
'''
    mail.send(msg)

