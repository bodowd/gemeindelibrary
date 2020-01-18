from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
# from gemlibapp.models import User


# class RegistrationForm(FlaskForm):
#     min_usr = 2
#     max_usr = 25
#     username = StringField(f'Username (between {min_usr} and {max_usr} characters)',
#                            validators=[DataRequired(), Length(min=min_usr, max=max_usr)])
#     email = StringField('Email', validators=[DataRequired(), Email()])
#     password = PasswordField('Password', validators=[DataRequired()])
#     # EqualTo must match the variable lowercase `password`!
#     confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
#     submit = SubmitField('Sign Up')
#
#     def validate_username(self, username):
#         """
#         Check if username is already existing
#         :param username:  StringField object
#         :return:
#         """
#         user = User.query.filter_by(username=username.data).first()
#         if user:
#             raise ValidationError('That username is taken. Please choose a different one.')
#
#     def validate_email(self, email):
#         """
#         Check if email is already existing
#         :param email:  StringField object
#         :return:
#         """
#         user = User.query.filter_by(email=email.data).first()
#         if user:
#             raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


# class UpdateAccountForm(FlaskForm):
#     min_usr = 2
#     max_usr = 25
#     username = StringField(f'Username (between {min_usr} and {max_usr} characters)',
#                            validators=[DataRequired(), Length(min=min_usr, max=max_usr)])
#     email = StringField('Email', validators=[DataRequired(), Email()])
#     submit = SubmitField('Update')
#
#     def validate_username(self, username):
#         """
#         Check if username is already existing
#         :param username:  StringField object
#         :return:
#         """
#         # check if the user actually changed their username. If not, don't do DB lookup
#         if current_user.username != username.data:
#             user = User.query.filter_by(username=username.data).first()
#             if user:
#                 raise ValidationError('That username is taken. Please choose a different one.')
#
#     def validate_email(self, email):
#         """
#         Check if email is already existing
#         :param email:  StringField object
#         :return:
#         """
#         if current_user.email != email.data:
#             user = User.query.filter_by(email=email.data).first()
#             if user:
#                 raise ValidationError('That email is taken. Please choose a different one.')
#
#
# class RequestResetForm(FlaskForm):
#     email = StringField('Email', validators=[DataRequired(), Email()])
#     submit = SubmitField('Request Password Reset')
#
#     def validate_email(self, email):
#         """
#         Check if email is already existing
#         :param email:  StringField object
#         :return:
#         """
#         user = User.query.filter_by(email=email.data).first()
#         if user is None:
#             raise ValidationError('There is no account with that email. You must register first.')
#
#
# class ResetPasswordForm(FlaskForm):
#     password = PasswordField('Password', validators=[DataRequired()])
#     # EqualTo must match the variable lowercase `password`!
#     confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
#     submit = SubmitField('Reset Password')
