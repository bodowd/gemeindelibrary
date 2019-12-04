from flask import Blueprint, render_template, url_for, flash, redirect, request, abort
from flask_login import current_user, login_required
from gemlibapp import db, bcrypt
from gemlibapp.models import BookList, User
from gemlibapp.booklist.forms import BookListForm, CheckoutBookForm
from gemlibapp.booklist.utils import booklist_to_df
import numpy as np
import pandas as pd
from datetime import datetime, timedelta


booklist = Blueprint('booklist', __name__)


# add new booklist
@booklist.route('/upload_booklist', methods=['GET', 'POST'])
@login_required
def upload_booklist():
    form = BookListForm()
    if form.validate_on_submit():
        df = booklist_to_df(form.booklist_file)
        if df.shape[1] < 2:  # check to make sure there is more than one column
            flash(
                'Missing column. Please remember to have the book titles\
                 in the first column and the number available in the second column',
                'danger')
            return render_template('booklist.html', title='Book List', form=form)
        # add standardized column names
        df.columns = ['Title', 'Number_available']
        # check to see if the first column is filled with strings -- titles
        if df['Title'].dtype != np.object or df['Number_available'].dtype != np.int:
            flash('Please make sure book titles are in the first\
                column and number of books available in the second column', 'danger')
            return render_template('booklist.html', title='Book List', form=form)

        # remove existing booklist for this user
        BookList.query.filter(BookList.owner == current_user).delete()
        db.session.commit()
        # add to db -- add one by one since it's simple and the data sizes are small
        for _, row in df.iterrows():
            # creates a new row for each copy of the same title
            for count in range(row['Number_available']):
                if row['Number_available'] > 1:
                    title = row['Title'] + f'-Copy({count+1})'
                else:
                    title = row['Title']
                booklist_to_db = BookList(title=title,
                                          owner=current_user,
                                          available=True)
                db.session.add(booklist_to_db)
                db.session.commit()
        flash('Your book list has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('booklist.html', title='Book List', form=form)


def update_booklist():
    """
    Updates the booklist without losing information on books that are already checked out
    """
    # currently new_booklist resets count_available. If an user wants to update their booklist
    # without resetting the counts, then this won't work.
    # Perhaps a solution is to have a New booklist option, this one, and an Update BookList
    # page. In the update BookList page the database should just carry over from count_available
    pass


@booklist.route('/booklist/<string:username>', methods=['GET', 'POST'])
@login_required
def view_booklist(username):
    user = User.query.filter_by(username=username).first_or_404()
    if user != current_user:
        abort(403)
    booklist = BookList.query.filter_by(owner=user).all()
    # df = pd.DataFrame(booklist)

    # might be a nicer way to do this, but this works
    booklist_dict = {}
    booklist_dict['Title'] = []
    booklist_dict['Available'] = []
    booklist_dict['Date Borrowed'] = []
    booklist_dict['Username'] = []
    booklist_dict['Borrower'] = []
    booklist_dict['Borrower Email'] = []
    booklist_dict['Date Due'] = []

    for book in booklist:
        booklist_dict['Title'].append(book.title)
        booklist_dict['Available'].append(book.available)
        booklist_dict['Date Borrowed'].append(book.date_borrowed)
        booklist_dict['Username'].append(book.owner.username)
        booklist_dict['Borrower'].append(book.borrower)
        booklist_dict['Borrower Email'].append(book.borrower_email)
        booklist_dict['Date Due'].append(book.date_due)

    df = pd.DataFrame.from_dict(booklist_dict)

    return render_template('view_booklist.html', title='Home',
                           tables=[df.to_html(classes='data', header='true')])


@booklist.route('/booklist/<string:username>/checkout', methods=['GET', 'POST'])
@login_required
def checkout_book(username):
    user = User.query.filter_by(username=username).first_or_404()
    if user != current_user:
        abort(403)
    booklist = BookList.query.filter_by(owner=user).all()

    form = CheckoutBookForm()

    # Drop down menu
    # needs to receive a tuple. I don't know why.
    form.title.choices = [(book.title, book.title) for book in booklist]

    if form.validate_on_submit():
        book = BookList.query.filter_by(title=form.title.data).first_or_404()
        book.borrower = form.borrower.data
        book.borrower_email = form.borrower_email.data
        book.available = False
        book.date_borrowed = datetime.utcnow().date()
        book.date_due = book.date_borrowed + timedelta(days=30)
        db.session.commit()
        flash(f'{book.title} has been checked out by {book.borrower}!', 'success')
        return redirect(url_for('main.home'))
    return render_template('checkout_book.html', title='Checkout Book', form=form)


@booklist.route('/booklist/<string:username>/return', methods=['GET', 'POST'])
@login_required
def return_book(username):
    pass
    # only populate the form with Books that are available=False
    # return render_template('return_book.html', title='Book Return', form=form)


