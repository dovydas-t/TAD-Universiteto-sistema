
from flask_login import UserMixin
from app.extensions import db, bcrypt, datetime, timedelta

# Define UserAuth DataModel. Make sure to add flask_user UserMixin!!
class AuthUser(UserMixin, db.Model):
    """User model for auth details"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String((255)), unique=True, nullable=False)
    password_hash = db.Column(db.String((255)))
    

    failed_login_attempts = db.Column(db.Integer, default=0, nullable=False)
    last_failed_login = db.Column(db.DateTime, nullable=True)
    blocked_until = db.Column(db.DateTime, nullable=True)
   
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)

    profile = db.relationship('UserProfile', back_populates='user', uselist=False, cascade="all, delete-orphan")
    
    def set_password(self, password):
        """Set user's password"""
        self.password_hash = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        """Check user's password"""
        return bcrypt.check_password_hash(self.password_hash, password)
    
    def is_blocked(self):
        if self.blocked_until:
            return datetime.utcnow() < self.blocked_until
        return False
    
    def record_failed_login(self):
        self.failed_login_attempts += 1
        self.last_failed_login = datetime.utcnow()
        # Block after 3 attempts for 15 minutes
        if self.failed_login_attempts >= 3:
            self.blocked_until = datetime.utcnow() + timedelta(minutes=15)
        db.session.commit()

    def record_successful_login(self):
        self.failed_login_attempts = 0
        self.last_failed_login = None
        self.blocked_until = None
        self.last_login = datetime.utcnow()
        db.session.commit()
    
    def get_time_until_unblock(self):
        if self.blocked_until and self.is_blocked():
            remaining = self.blocked_until - datetime.utcnow()
            return int(remaining.total_seconds() / 60) + 1
        return 0
    
    def __repr__(self):
        return f'<User {self.username}>'

def create_hardcoded_admin():
    """Create the initial hardcoded administrator"""
    admin = AuthUser.query.filter_by(username='admin').first()
    if not admin:
        admin = AuthUser(
            username='admin',
            is_admin=True,
            is_active=True  # Make sure it's active
        )
        admin.set_password('admin123')  # Change this password!
        db.session.add(admin)
        db.session.commit()
        print("Hardcoded admin created: username='admin', password='admin123'")
    return admin