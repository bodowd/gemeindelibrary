from datetime import datetime, timedelta
from gemlibapp import db, login_manager
from flask import current_app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

'''
During development, if you need to recreate database...
>>> from gemlibapp import create_app
>>> from gemlibapp import db
>>> db.create_all(app=create_app())
'''


# decorator lets login_manager package find the user in the session
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)  # we will hash this
    # relationship to the Post Model. username attribute will get us back to the user who made the post
    # lazy loads the data as necessary in one go
    # we would not see this "booklist" in a SQL viewer. it's making a query here
    # BookList is capitalized because we are referencing the BookList class not a table
    # user.booklist should return their books -- links to BookList table
    booklists = db.relationship('BookList', backref='owner', lazy=True)
    reminders = db.relationship('Reminder', backref='owner', lazy=True)

    def __repr__(self):
        # how our object is printed when printed out
        return f"User('{self.username}', '{self.email}')"

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    # doesn't need the self argument
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)


class BookList(db.Model):
    """
     SQLALCHEMY automatically creates the table name by
     converting adding an underscore between
     camel case and making it all lower
     """

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    available = db.Column(db.Boolean, nullable=False)
    # user.id is lower case because we are referencing the table.column name
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    borrower = db.Column(db.String(100), nullable=True)
    # unique=False person may borrow multiple books
    borrower_email = db.Column(db.String(120), unique=False, nullable=True)
    date_borrowed = db.Column(db.Date, nullable=True)
    date_due = db.Column(db.Date, nullable=True)

    def __repr__(self):
        return f"Books('{self.title}', '{self.available}', '{self.date_borrowed}', '{self.user_id}')"


class Reminder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # to link back to `user` Table
    message = db.Column(db.Text, nullable=False)
    subject = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Reminder Table('{self.subject}', '{self.message}')"
