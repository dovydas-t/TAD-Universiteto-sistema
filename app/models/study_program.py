from app.extensions import db


class StudyProgram(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.id'))
    
    faculty = db.relationship('Faculty', back_populates='programs')
    groups = db.relationship('Groups', back_populates='study_program')
    modules = db.relationship('Module', back_populates='study_program')
    users = db.relationship('UserProfile', back_populates="study_program")

    def __repr__(self):
        return f"Study Program('{self.name}', Study Program ID: {self.id})"