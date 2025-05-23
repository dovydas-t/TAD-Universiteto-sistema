from datetime import datetime
from flask_login import UserMixin
from app.extensions import db


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user_id = db.Column(db.Integer, db.ForeignKey('auth_user.id'), nullable=False)

    creator = db.relationship('AuthUser', back_populates='posts')

    def __repr__(self):
        return f"Post('{self.title}', User ID: {self.user_id})"