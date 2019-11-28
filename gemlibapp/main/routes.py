from flask import Blueprint, render_template, request

from gemlibapp.models import BookList

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    # posts = Post.query.order_by(Post.date_posted.desc()).paginate(per_page=3, page=page)
    return render_template('home.html')


@main.route('/about')
def about():
    return render_template('about.html', title='About')








