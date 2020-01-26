import os
from flask import Blueprint, render_template, url_for, flash, redirect, request, abort
from flask_login import current_user, login_required
from flask_mail import Message
from gemlibapp import db, bcrypt, mail
from gemlibapp.models import BookList, BookStatus, credentials
from gemlibapp.booklist.forms import BookListForm, CheckoutBookForm, ReturnBookForm, DeleteBookListForm
from gemlibapp.booklist.utils import booklist_to_df, validate_standardize, booklist2df
from gemlibapp.config import Config
import pandas as pd
from datetime import datetime, timedelta

booklist = Blueprint('booklist', __name__)


@booklist.route('/delete_booklist', methods=['GET', 'POST'])
@login_required
def delete_booklist():
    '''removes existing booklist !!!'''

    # TODO: add password verification as safety
    form = DeleteBookListForm()
    if form.validate_on_submit():
        BookList.query.delete()

        db.session.commit()
        flash('Your book list has been deleted.', 'success')
        return redirect(url_for('main.home'))
    return render_template('delete_booklist.html', title='Delete Booklist', form=form)


# ### JUST FOR DEV!!
# @booklist.route('/delete_status', methods=['GET', 'POST'])
# @login_required
# def delete_status():
#     ### TEMPORARY JUST FOR DEV
#     BookStatus.query.delete()
#     return redirect(url_for('main.home'))

@booklist.route('/upload_booklist', methods=['GET', 'POST'])
@login_required
def upload_booklist():
    form = BookListForm()
    if form.validate_on_submit():
        df = booklist_to_df(form.booklist_file)
        df = validate_standardize(df, form)
        if df is None:
            return render_template('booklist.html', title='Book List', form=form)

        # adds books iteratively
        for _, row in df.iterrows():
            title = row['Title']
            _book = BookList.query.filter_by(title=title).first()
            # only add to db if it doesn't already exist in db
            if _book is None:
                booklist_to_db = BookList(title=title)
                db.session.add(booklist_to_db)
                db.session.commit()
            # creates new book status if it's not already in book_status table
            # if it is already there, we skip it so that we don't lose information on currently checked out books
            _book = BookList.query.filter_by(title=title).first()
            book_status = BookStatus.query.filter_by(book_id=_book.id).first()
            if book_status is None:
                _status = BookStatus(book_id=_book.id, available=True, borrower=None, back2booklist=_book)
                db.session.add(_status)
        db.session.commit()
        flash('Your book list has been updated!', 'success')
        return redirect(url_for('main.home'))
    return render_template('booklist.html', title='Book List', form=form)


@booklist.route('/booklist', methods=['GET'])
@login_required
def view_booklist():
    booklist = BookList.query.all()
    ### reminder of how to parse the output of a sqlalchemy query ... # print(booklist[0].title)
    # df = pd.DataFrame(booklist)

    # might be a nicer way to do this, but this works
    booklist_dict = {}
    booklist_dict['Title'] = []
    booklist_dict['Available'] = []
    booklist_dict['Date Borrowed'] = []
    booklist_dict['Borrower'] = []
    booklist_dict['Borrower Email'] = []
    booklist_dict['Date Due'] = []

    for book in booklist:
        book_status = BookStatus.query.filter_by(book_id=book.id).first()
        booklist_dict['Title'].append(book.title)
        booklist_dict['Available'].append(book_status.available)
        booklist_dict['Date Borrowed'].append(book_status.date_borrowed)
        booklist_dict['Borrower'].append(book_status.borrower)
        booklist_dict['Borrower Email'].append(book_status.borrower_email)
        booklist_dict['Date Due'].append(book_status.date_due)

    df = pd.DataFrame.from_dict(booklist_dict)

    return render_template('view_booklist.html', title='Home',
                           tables=[df.to_html(classes='data', header='true')])


@booklist.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout_book():
    # get the books that are available
    # booklist = BookList.query.all()
    _status = BookStatus.query.filter_by(available=True).all()
    form = CheckoutBookForm()

    # Drop down menu
    # needs to receive a tuple. I don't know why.
    form.title.choices = [(book.back2booklist.title, book.back2booklist.title) for book in _status if
                          BookList.query.filter_by(id=book.id).first() is not None]
    # needs to check if we have a status stored but we don't have it in the booklist

    if form.validate_on_submit():
        # get the object from booklist
        title = BookList.query.filter_by(title=form.title.data).first_or_404()
        # pass that object to status via the backref back2booklist to check it out
        book = BookStatus.query.filter_by(back2booklist=title).first_or_404()
        book.borrower = form.borrower.data
        book.borrower_email = form.borrower_email.data
        book.available = False
        book.date_borrowed = datetime.utcnow().date()
        book.date_due = book.date_borrowed + timedelta(days=30)
        db.session.commit()

        flash(f'{book.back2booklist.title} has been checked out by {book.borrower}!', 'success')
        return redirect(url_for('main.home'))

    return render_template('checkout_book.html', title='Checkout Book', form=form)


@booklist.route('/return_book', methods=['GET', 'POST'])
@login_required
def return_book():
    # booklist = BookList.query.filter_by(owner=user).all()
    _status = BookStatus.query.filter_by(available=False).all()

    form = ReturnBookForm()

    # only populate the form with Books that are available=False
    form.title.choices = [(book.back2booklist.title, book.back2booklist.title) for book in _status if
                          BookList.query.filter_by(id=book.id).first() is not None]
    # needs to check if we have a status stored but we don't have it in the booklist

    if form.validate_on_submit():
        # get the object from booklist
        title = BookList.query.filter_by(title=form.title.data).first_or_404()
        # pass that object to status via the backref back2booklist to check it out
        book = BookStatus.query.filter_by(back2booklist=title).first_or_404()
        book.borrower = None
        book.borrower_email = None
        book.available = True
        book.date_borrowed = None
        book.date_due = None
        db.session.commit()

        flash(f'{book.back2booklist.title} has been returned.', 'success')
        return redirect(url_for('main.home'))

    return render_template('return_book.html', title='Book Return', form=form)


@booklist.route('/booklist/backup')
def backup_current_booklist():
    '''
    Backs up current status and sends it to admin email

    This will be called via crontab by wget -O- httppath/to/here

    Remember to access crontab on the server with sudo
    '''
    df = booklist2df()
    # make tmp file and put it in tmp directory. After sending the email it will be deleted
    path_tmp = os.path.join(Config.PYTHONPATH, 'gemlibapp', 'booklist', 'tmp')
    csv_filename = f'backup_{datetime.utcnow().date()}.csv'
    df.to_csv(os.path.join(path_tmp, csv_filename))

    with open(os.path.join(path_tmp, csv_filename), 'r') as f:
        msg = Message(subject=f'Library backup {datetime.utcnow().date()}', sender=Config.MAIL_USERNAME,
                      recipients=[Config.MAIL_USERNAME])
        msg.body = 'Please find a backup of the library in the attachments.' \
                   '\nIm Anhang findest du bitte die Bibliothek.'
        msg.attach(filename=csv_filename, content_type='text/csv', data=f.read())
        mail.send(msg)

    # cleanup tmp dir
    filelist = [f for f in os.listdir(path_tmp) if f.endswith('.csv')]
    for f in filelist:
        os.remove(os.path.join(path_tmp, f))

    return redirect(url_for('main.home'))
