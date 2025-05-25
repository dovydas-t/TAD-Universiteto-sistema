from app.extensions import db

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user_profile.id'))
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'))
    date = db.Column(db.Date)
    present = db.Column(db.Boolean)

    student = db.relationship("UserProfile", back_populates="attendances")
    module = db.relationship("Module", back_populates="attendances")