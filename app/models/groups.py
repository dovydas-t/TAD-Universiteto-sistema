from app.extensions import db

#Pavadinau Groups, nes nerekomenduoja naudoti Group kaip pavadinimo :D
class Groups(db.Model):
    _tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(255))
    study_program_id = db.Column(db.Integer, db.ForeignKey('study_program.id'))

    study_program = db.relationship("StudyProgram", back_populates="groups")
    users = db.relationship("UserProfile", back_populates="group")