from app.extensions import db

class Groups(db.Model):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(255))
    study_program_id = db.Column(db.Integer, db.ForeignKey('study_program.id'))
    max_capacity = db.Column(db.Integer, nullable=False )

    study_program = db.relationship("StudyProgram", back_populates="groups")
    users = db.relationship("UserProfile", back_populates="group")