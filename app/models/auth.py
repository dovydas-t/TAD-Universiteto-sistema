from datetime import datetime
from flask_login import UserMixin
from app.extensions import db, bcrypt

# Define UserAuth DataModel. Make sure to add flask_user UserMixin!!
class AuthUser(UserMixin, db.Model):
    """User model for auth details"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String((255)), unique=True, nullable=False)
    password_hash = db.Column(db.String((255)))

    profile = db.relationship('UserProfile', back_populates='user', uselist=False, cascade="all, delete-orphan")
    
    def set_password(self, password):
        """Set user's password"""
        self.password_hash = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        """Check user's password"""
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'
