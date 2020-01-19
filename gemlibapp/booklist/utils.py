import pandas as pd
import os
from flask import flash
import numpy as np
from gemlibapp.models import BookList, BookStatus

def booklist_to_df(booklist_file):
    _, f_ext = os.path.splitext(booklist_file.data.filename)
    _data = booklist_file.data.stream
    if f_ext == '.xlsx':
        # remove header and index incase
        df = pd.read_excel(_data)
    elif f_ext == '.txt':
        df = pd.read_csv(_data, delimiter='\t')
    return df

def validate_standardize(df, form):
    if df.shape[1] != 1:  # check to make sure there is only one column
        # print(df.shape)
        flash('Please make sure to only submit one column which is composed of book titles.', 'danger')
        return None
    # add standardized column names

    df.columns = ['Title']
    if df['Title'].nunique() != df.shape[0]:
        flash('Please make sure every book title is unique with your own labeling.', 'danger')
    # check to see if the first column is filled with strings -- titles
    if df['Title'].dtype != np.object:
        flash('Please make sure the column of titles is filled.', 'danger')
        return None
    df = df.sort_values(by=['Title'])
    return df

def booklist2df():
    '''
    Gets the booklist and statuses from database and converts it to a pandas dataframe
    :return:
    '''

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
    return df
