import pandas as pd
import os
from flask import flash
import numpy as np

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

