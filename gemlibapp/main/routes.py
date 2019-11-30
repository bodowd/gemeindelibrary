from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('booklist.view_booklist', username=current_user.username))

    # page = request.args.get('page', 1, type=int)
    # posts = Post.query.order_by(Post.date_posted.desc()).paginate(per_page=3, page=page)
    else:
        return render_template('home.html')


@main.route('/about')
def about():
    return render_template('about.html', title='About')








