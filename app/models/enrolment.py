from app.extensions import db
from datetime import datetime

class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user_profile.id'))
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'))
    enrollment_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='enrolled')