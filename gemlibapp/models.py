from datetime import datetime, timedelta
from gemlibapp import db, login_manager
from flask import current_app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from gemlibapp.config import Config

'''
During development, if you need to recreate database...
>>> from gemlibapp import create_app
>>> from gemlibapp import db
>>> db.create_all(app=create_app())
'''

# TODO: add migration

class User(UserMixin):
    pass


credentials = {'email': Config.APP_USERNAME,
               'password': Config.APP_PASSWORD}


# # decorator lets login_manager package find the user in the session
@login_manager.user_loader
def load_user(email):
    if email != credentials['email']:
        return None
    user = User()  # UserMixin class contains methods needed by flask-login
    # user.id = email
    return user


class BookList(db.Model):
    """
     SQLALCHEMY automatically creates the table name by
     converting adding an underscore between
     camel case and making it all lower
     """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"{self.__dict__}"


class BookStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # booklist.id is lower case because we are referencing the table.column name
    book_id = db.Column(db.Integer, db.ForeignKey('book_list.id'), nullable=False)
    backup_title = db.Column(db.String(100), nullable=False)
    available = db.Column(db.Boolean, nullable=False)
    borrower = db.Column(db.String(100), nullable=True)
    # unique=False person may borrow multiple books
    borrower_email = db.Column(db.String(120), unique=False, nullable=True)
    date_borrowed = db.Column(db.Date, nullable=True)
    date_due = db.Column(db.Date, nullable=True)

    def __repr__(self):
        return f"{self.__dict__}"


class Reminder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # to link back to `user` Table
    message = db.Column(db.Text, nullable=False)
    subject = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Reminder Table('{self.subject}', '{self.message}')"
