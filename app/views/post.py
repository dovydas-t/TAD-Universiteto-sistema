from flask import Blueprint, request, redirect, render_template
from flask_login import login_required, current_user
from app.services.post_service import create_post, get_post, update_post, delete_post, get_all_posts
from app.forms.post import PostForm
from app.models.post import Post


bp = Blueprint('posts', __name__)

@bp.route('/')
def index():
    posts = get_all_posts()
    return render_template('posts/posts.html', title='Posts', posts=posts)

@bp.route('/new_post', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        create_post(title, content, current_user.id)
        return redirect('/posts')
    
    return render_template('posts/new_post.html', form=form)

@bp.route('/post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def post_detail(post_id):
    post = get_post(post_id)
    return render_template('posts/post_detail.html', post=post)


# @bp.route('/profile/update', methods=['GET', 'POST'])
# @login_required
# def profile_update():
#     """User profile update"""
#     form = ProfileForm(obj=current_user.profile)    
#     if form.validate_on_submit():
#         user_changed = (
#             form.username.data != current_user.username or
#             form.first_name.data != current_user.profile.first_name or
#             form.last_name.data != current_user.profile.last_name or
#             form.email.data != current_user.profile.email or
#             form.birth_date.data != current_user.profile.birth_date
#         )

#         if not user_changed:
#             flash("No changes detected.", "info")
#             return redirect(url_for('main.profile'))

#         # Proceed with updating only if something changed
#         current_user.username = form.username.data
#         current_user.profile.first_name = form.first_name.data
#         current_user.profile.last_name = form.last_name.data
#         current_user.profile.email = form.email.data
#         current_user.profile.birth_date = form.birth_date.data

#         db.session.commit()
#         flash("Profile updated successfully!", "success")
#         return redirect(url_for('main.profile'))

#     return render_template("main/update_profile.html", form=form)