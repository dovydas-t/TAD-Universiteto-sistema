from app.extensions import db

class Grade(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user_profile.id'))
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'))
    grade = db.Column(db.Float)


    student = db.relationship("UserProfile", back_populates="grades")
    module = db.relationship("Module", back_populates="grades")