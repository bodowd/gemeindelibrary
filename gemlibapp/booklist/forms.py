from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import SubmitField, SelectField, StringField
from wtforms.validators import DataRequired, Email


class BookListForm(FlaskForm):
    """
    User shall submit a excel or csv file. Parsed in booklist.routes

    Format should be Book Title, Number of available.
    Headers should be included.

    Will strip the header below to standardize the naming. But the order needs to be like this

    """
    allowed_ext = ['xlsx', 'txt']  # file should be tab delimited incase book titles have commas in them
    booklist_file = FileField('Submit booklist file',
                              validators=[DataRequired(), FileAllowed(allowed_ext)])
    submit = SubmitField('Create Book List')


class UpdateBookListForm(FlaskForm):
    allowed_ext = ['xlsx', 'txt']  # file should be tab delimited incase book titles have commas in them
    booklist_file = FileField('Submit booklist file',
                              validators=[DataRequired(), FileAllowed(allowed_ext)])
    submit = SubmitField('Update Book List')


class CheckoutBookForm(FlaskForm):
    # coerce to str so that the returned value in form.title.data is the book title
    title = SelectField('Title', coerce=str)
    borrower = StringField('Borrower', validators=[DataRequired()])
    borrower_email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Checkout Book')
