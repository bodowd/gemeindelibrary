from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import current_user, login_required
from gemlibapp import db, bcrypt
from gemlibapp.models import BookList, User
from gemlibapp.booklist.forms import BookListForm
from gemlibapp.booklist.utils import booklist_to_df
import numpy as np
import pandas as pd

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
            print(row['Number_available'])
            for count in range(row['Number_available']):
                booklist_to_db = BookList(title=row['Title'],
                                          owner=current_user,
                                          available=True)
                db.session.add(booklist_to_db)
                db.session.commit()
        flash('Your book list has been created!', 'success')
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
    booklist = BookList.query.filter_by(owner=user).all()
    # df = pd.DataFrame(booklist)

    # might be a nicer way to do this, but this works
    booklist_dict = {}
    booklist_dict['Title'] = []
    booklist_dict['Available'] = []
    booklist_dict['Date Borrowed'] = []
    booklist_dict['Username'] = []
    for book in booklist:
        booklist_dict['Title'].append(book.title)
        booklist_dict['Available'].append(book.available)
        booklist_dict['Date Borrowed'].append(book.date_borrowed)
        booklist_dict['Username'].append(user.username)

    df = pd.DataFrame.from_dict(booklist_dict)
    return render_template('view_booklist.html', title='Home',
                           tables=[df.to_html(classes='data', header='true')])

