from flask import Blueprint, request, redirect, render_template
from flask_login import login_required, current_user
from app.services.post_service import create_post, get_post, update_post, delete_post, get_all_posts

bp = Blueprint('posts', __name__)

@bp.route('/')
def index():
    posts = get_all_posts()
    return render_template('posts/posts.html', title='Posts', posts=posts)

@bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        create_post(title, content, current_user.id)
        return redirect('/posts')
    return render_template('posts/new.html')
