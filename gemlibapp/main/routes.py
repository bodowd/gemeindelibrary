from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('booklist.view_booklist'))
    else:
        return render_template('home.html')


@main.route('/about')
def about():
    return render_template('about.html', title='About')








