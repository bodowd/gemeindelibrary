from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from gemlibapp import db, bcrypt
from gemlibapp.models import User, BookList
from gemlibapp.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm)
from gemlibapp.users.utils import send_reset_email

users = Blueprint('users', __name__)


@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # hash password
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # create new instance of user - validation is done in forms.py
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('users.login'))  # home is the name of the FUNCTION of that route
    return render_template('register.html', title='Register', form=form)


@users.route('/login', methods=['GET', 'POST'])
def login():
    # if logged in already just go to home page
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        # query database to see if user exists
        user = User.query.filter_by(email=form.email.data).first()  # return first user that matches
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            # return the user, after they log in, to the page they were trying to get to but weren't logged in
            next_page = request.args.get('next')
            flash('You have successfully logged in. Welcome back.', 'success')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            # danger is bootstrap class
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@users.route('/logout')
def logout():
    logout_user()
    flash('You have logged out.', 'success')
    return redirect(url_for('main.home'))


@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    ''' login_required decorator checks to see if user is logged in already'''
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        # post-get-redirect pattern "Are you sure you want to reload? Data will be resubmitted"
        return redirect(url_for('users.account'))
    # populate form fields with current user data if method is just GET
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account.html', title='Account', form=form)


@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    # want to make sure the user is logged out before resetting password
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    # if user has submitted a valid email, get the user
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    # want to make sure the user is logged out before resetting password
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token.', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        # hash password
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # create new instance of user - validation is done in forms.py
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in.', 'success')
        return redirect(url_for('users.login'))  # home is the name of the FUNCTION of that route
    return render_template('reset_token.html', title='Reset Password', form=form)
