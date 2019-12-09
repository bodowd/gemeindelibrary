from flask import url_for
from flask_mail import Message
import gemlibapp
from gemlibapp.config import Config




def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message(subject='Password Reset Request', sender=Config.MAIL_USERNAME, recipients=[user.email])
    # _external=True gives an absolute url rather than a relative url. Gives full domain
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    gemlibapp.mail.send(msg)
