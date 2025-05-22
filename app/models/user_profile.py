from datetime import datetime
from app.extensions import db


class UserProfile(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('auth_user.id'), primary_key=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    birth_date = db.Column(db.Date, nullable=True)
    email = db.Column(db.String(35), unique=True, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    last_login = db.Column(db.DateTime)

    def __repr__(self):
        return f"UserProfile('{self.id}', '{self.created_at}')"

    @property
    def full_name(self):
        """Get user's full name"""  
        return f"{self.first_name or ''} {self.last_name or ''}".strip() or self.user.username
