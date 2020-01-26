'''
Just handles login and logout
'''

from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from gemlibapp import db, bcrypt, login_manager
from gemlibapp.models import BookList, User, credentials
from gemlibapp.users.forms import LoginForm

users = Blueprint('users', __name__)

@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in credentials:
        return

    user = User()
    user.id = email

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = request.form['password'] == credentials['password']
    return user


@users.route('/login', methods=['GET', 'POST'])
def login():
    # if logged in already just go to home page
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == credentials['email'] and form.password.data == credentials['password']:
            user = User()
            user.id = form.email.data
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


