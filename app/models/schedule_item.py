from app.extensions import db

class ScheduleItem(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_profile.id')) 
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'))
    type = db.Column(db.String(255))  # e.g., 'Lecture', 'Exam'
    date = db.Column(db.DateTime)

    module = db.relationship("Module", back_populates="schedule_items")
    user = db.relationship("UserProfile", back_populates="schedule_items")