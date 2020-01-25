from flask import Blueprint, render_template, url_for, flash, redirect, abort, request
from flask_login import current_user, login_required
from gemlibapp.models import User, Reminder, BookList
from gemlibapp.reminder.forms import ReminderEmailForm
from gemlibapp import db
from datetime import datetime, timedelta
from gemlibapp.reminder.utils import send_reminder_email, DefaultReminderMessage

reminder = Blueprint('reminder', __name__)

@reminder.route('/reminder_email', methods=['GET', 'POST'])
@login_required
def reminder_email():

    form = ReminderEmailForm()
    if form.validate_on_submit():
        current_message = Reminder.query.first()
        # store template in db
        current_message.message = form.message.data
        current_message.subject = form.subject.data
        db.session.commit()
        flash('The content in your reminder email has been updated.', 'success')

    elif request.method == 'GET':
        current_message = Reminder.query.first()
        if current_message is None:
            reminder_db = Reminder(message=DefaultReminderMessage.default_message,
                                   subject=DefaultReminderMessage.default_subject)
            db.session.add(reminder_db)
            db.session.commit()
            return redirect(url_for('reminder.reminder_email'))
        else:
            form.message.data = current_message.message
            form.subject.data = current_message.subject

    return render_template('reminder_email.html', title='Reminder Email', form=form)


@reminder.route('/daily_check')
def daily_check():
    """
    Checks for books due 7 days from today.
    wget -O- the_website.com/daily_check will be called from crontab every day

    """
    # # to test functionality:
    #due_date = datetime.today() + timedelta(days=7)

    # production
    due_date = datetime.today() + timedelta(days=30)
    books_due = BookList.query.filter_by(date_due=due_date.date()).all()
    for book in books_due:
        # couldn't filter_by owner because that doesn't take strings. That takes `current_user` object
        id_user = User.query.filter_by(username=book.owner.username).first().id
        # get the booklist owner's reminder email message and subject
        _reminder = Reminder.query.filter_by(user_id=id_user).first()
        subject = _reminder.subject
        message = _reminder.message
        send_reminder_email(book.borrower_email, subject=subject, message=message)
    return redirect(url_for('main.home'))

