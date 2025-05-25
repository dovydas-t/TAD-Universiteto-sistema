from app.models.study_program import Post
from app.extensions import db

def create_post(title, content, user_id):
    post = Post(title=title, content=content, user_id=user_id)
    db.session.add(post)
    db.session.commit()
    return post

def get_post(post_id):
    return Post.query.get(post_id)

def update_post(post_id, title=None, content=None):
    post = Post.query.get(post_id)
    if post:
        if title:
            post.title = title
        if content:
            post.content = content
        db.session.commit()
    return post

def delete_post(post_id):
    post = Post.query.get(post_id)
    if post:
        db.session.delete(post)
        db.session.commit()
    return post

def get_all_posts():
    posts = Post.query.all()
    if posts:
        return posts