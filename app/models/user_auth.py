from sqlalchemy import event
from datetime import datetime
from flask_login import UserMixin
from app.extensions import db, bcrypt


class AuthUser(UserMixin, db.Model):
    """User model for auth details"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    profile = db.relationship('UserProfile', backref='user', uselist=False, cascade="all, delete-orphan")
    posts = db.relationship('Post', backref='creator', lazy=True)

    def set_password(self, password):
        """Set user's password"""
        self.password_hash = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        """Check user's password"""
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'
    
# # Create user.profile automatically when user is created
# @event.listens_for(AuthUser, 'after_insert')
# def create_user_profile(mapper, connection, target):
#     """Automatically create a UserProfile when AuthUser is created"""
#     from app.models.user_profile import UserProfile
    
#     profile = UserProfile() #Leave empty UserProfile() for Default to set at created_at
#     db.session.add(profile)
#     db.session.commit()