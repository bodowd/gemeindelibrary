from flask import Blueprint, render_template, url_for, flash, redirect, request, abort
from flask_login import current_user, login_required
from gemlibapp import db, bcrypt
from gemlibapp.models import BookList, User
from gemlibapp.booklist.forms import BookListForm, CheckoutBookForm, ReturnBookForm, UpdateBookListForm
from gemlibapp.booklist.utils import booklist_to_df, validate_standardize
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
        df = validate_standardize(df, form)
        if df is None:
            return render_template('booklist.html', title='Book List', form=form)
        # removes existing booklist for this user !!!
        # TODO: Add a function to back up current checkout lists
        BookList.query.filter(BookList.owner == current_user).delete()
        db.session.commit()
        # add to db -- add one by one since it's simple and the data sizes are small
        for _, row in df.iterrows():
            title = row['Title']
            booklist_to_db = BookList(title=title,
                                      owner=current_user,
                                      available=True)
            db.session.add(booklist_to_db)
            db.session.commit()
        flash('Your book list has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('booklist.html', title='Book List', form=form)

@booklist.route('/update_booklist', methods=['GET', 'POST'])
@login_required
def update_booklist():
    """
    Updates the booklist without losing information on books that are already checked out
    """
    # currently new_booklist resets count_available. If an user wants to update their booklist
    # without resetting the counts, then this won't work.
    # Perhaps a solution is to have a New booklist option, this one, and an Update BookList
    # page. In the update BookList page the database should just carry over from count_available
    form = UpdateBookListForm()
    if form.validate_on_submit():
        df = booklist_to_df(form.booklist_file)
        df = validate_standardize(df, form)
        if df is None:
            return render_template('booklist.html', title='Book List', form=form)
        for _, row in df.iterrows():
            title = row['Title']
            # # creates a new row for each copy of the same title
            # for count in range(row['Number_available']):
            #     if row['Number_available'] > 1:
            #         title = row['Title'] + f'-Copy({count+1})'
            #     else:
            #         title = row['Title']

            check_if_exists = BookList.query.filter_by(title=title).all()
            print(check_if_exists)
            print(check_if_exists is None)
            # if the book is not already in the database, add it
            if check_if_exists is None:
                print(title)
                booklist_to_db = BookList(title=title,
                                          owner=current_user,
                                          available=True)
                db.session.add(booklist_to_db)
                db.session.commit()
            # elif check_if_exists.title == title:

        flash('Your book list has been updated!', 'success')
        return redirect(url_for('main.home'))
    return render_template('update_booklist.html', title='Upload Booklist', form=form)




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
    form.title.choices = [(book.title, book.title) for book in booklist if book.available]

    if form.validate_on_submit():
        book = BookList.query.filter_by(title=form.title.data, owner=user).first_or_404()
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
    user = User.query.filter_by(username=username).first_or_404()
    if user != current_user:
        abort(403)
    booklist = BookList.query.filter_by(owner=user).all()

    form = ReturnBookForm()

    # only populate the form with Books that are available=False
    form.title.choices = [(book.title, book.title) for book in booklist if not book.available]

    if form.validate_on_submit():
        book = BookList.query.filter_by(title=form.title.data, owner=user).first_or_404()
        book.borrower = None
        book.borrower_email = None
        book.available = True
        book.date_borrowed = None
        book.date_due = None
        db.session.commit()

        flash(f'{book.title} has been returned.', 'success')
        return redirect(url_for('main.home'))

    return render_template('return_book.html', title='Book Return', form=form)


