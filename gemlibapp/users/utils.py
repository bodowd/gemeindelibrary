import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
import gemlibapp




def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message(subject='Password Reset Request', sender='odowd.bing@gmail.com', recipients=[user.email])
    # _external=True gives an absolute url rather than a relative url. Gives full domain
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    gemlibapp.mail.send(msg)
