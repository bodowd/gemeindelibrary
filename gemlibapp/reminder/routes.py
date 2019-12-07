from flask import Blueprint, render_template, url_for, flash, redirect, abort, request
from flask_login import login_user, current_user, login_required
from gemlibapp.models import User, Reminder
from gemlibapp.reminder.forms import ReminderEmailForm
from gemlibapp import db
from gemlibapp.reminder.utils import send_reminder_email

reminder = Blueprint('reminder', __name__)

@reminder.route('/reminder_email/<string:username>', methods=['GET', 'POST'])
@login_required
def reminder_email(username):
    user = User.query.filter_by(username=username).first_or_404()
    if user != current_user:
        abort(403)

    form = ReminderEmailForm()
    if form.validate_on_submit():
        current_message = Reminder.query.filter_by(owner=user).first()
        # store template in db
        current_message.message = form.message.data
        db.session.commit()
        flash('The content in your reminder email has been updated.', 'success')

    elif request.method == 'GET':
        current_message = Reminder.query.filter_by(owner=user).first()
        if current_message is None:
            reminder_db = Reminder(message=default_message,
                                   owner=current_user)
            db.session.add(reminder_db)
            db.session.commit()
            return redirect(url_for('reminder.reminder_email', username=username))
        else:
            form.message.data = current_message.message


    return render_template('reminder_email.html', title='Reminder Email', form=form)

default_message = """Liebe Heilige,
das von dir ausgeliehene Buch ist fällig.
Bitte vergisst du nicht, es zurückzusenden.
Vielen Dank.

Hello Saint,
The book you have borrowed is due.
Please do not forget to return it.
Thank you.
"""
# @users.route('/reset_password', methods=['GET', 'POST'])
# def reset_request():
#     # want to make sure the user is logged out before resetting password
#     if current_user.is_authenticated:
#         return redirect(url_for('main.home'))
#     form = RequestResetForm()
#     # if user has submitted a valid email, get the user
#     if form.validate_on_submit():
#         user = User.query.filter_by(email=form.email.data).first()
#         send_reset_email(user)
#         flash('An email has been sent with instructions to reset your password.', 'info')
#         return redirect(url_for('users.login'))
#
#
#     return render_template('reset_request.html', title='Reset Password', form=form)
#
