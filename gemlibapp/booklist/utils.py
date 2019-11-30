import pandas as pd
import os


def booklist_to_df(booklist_file):
    _, f_ext = os.path.splitext(booklist_file.data.filename)
    _data = booklist_file.data.stream
    if f_ext == '.xlsx':
        # remove header and index incase
        df = pd.read_excel(_data)
    elif f_ext == '.txt':
        df = pd.read_csv(_data, delimiter='\t')
    return df
