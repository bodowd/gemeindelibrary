from flask import Blueprint, render_template, url_for, flash, redirect, abort, request
from flask_login import login_user, current_user, login_required
from gemlibapp.models import User, Reminder, BookList
from gemlibapp.reminder.forms import ReminderEmailForm
from gemlibapp import db
from datetime import datetime, timedelta
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
        current_message.subject = form.subject.data
        db.session.commit()
        flash('The content in your reminder email has been updated.', 'success')

    elif request.method == 'GET':
        current_message = Reminder.query.filter_by(owner=user).first()
        if current_message is None:
            reminder_db = Reminder(message=default_message,
                                   owner=current_user,
                                   subject=default_subject)
            db.session.add(reminder_db)
            db.session.commit()
            return redirect(url_for('reminder.reminder_email', username=username))
        else:
            form.message.data = current_message.message
            form.subject.data = current_message.subject

    return render_template('reminder_email.html', title='Reminder Email', form=form)

default_message = """Liebe Heilige,
das von dir ausgeliehene Buch ist fällig.
Bitte vergisst du nicht, es zurückzusenden.
Vielen Dank.

Grüße,
Bücher dienende Heilige 
--------------
Hello Saint,
The book you have borrowed is due.
Please do not forget to return it.
Thank you.

Regards,
Saints serving with books
"""

default_subject = "Das Buch ist bald fällig. The book is due soon."

@reminder.route('/daily_check')
def daily_check():
    """ Checks for books due 7 days from today"""
    # # to test functionality:
    # due_date = datetime.today() + timedelta(days=30)

    due_date = datetime.today() + timedelta(days=7)
    books_due = BookList.query.filter_by(date_due=due_date.date()).all()
    for book in books_due:
        # couldn't filter_by owner because that doesn't take strings. That takes `current_user` object
        id_user = User.query.filter_by(username=book.owner.username).first().id
        _reminder = Reminder.query.filter_by(user_id=id_user).first()
        subject = _reminder.subject
        message = _reminder.message
        print(subject, message)
        send_reminder_email(book.borrower_email, subject=subject, message=message)
    return render_template('home.html')