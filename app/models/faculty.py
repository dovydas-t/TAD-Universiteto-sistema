from app.extensions import db

class Faculty(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))

    programs = db.relationship("StudyProgram", back_populates="faculty")

def __repr__(self):
    return f"<Faculty {self.id}: {self.name}>"
