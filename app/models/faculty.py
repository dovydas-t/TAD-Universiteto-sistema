from app.extensions import db

class Faculty(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    city = db.Column(db.String(100))
    street = db.Column(db.String(100))
    address = db.Column(db.String(255))  # Could be building number, room, etc.
    description = db.Column(db.Text)  # Long text field for details about the faculty


    programs = db.relationship("StudyProgram", back_populates="faculty")

    def get_full_address(self):
        parts = [self.street, self.address, self.city]
        return ' '.join(part for part in parts if part)

    def __repr__(self):
        return f"<Faculty {self.id}: {self.name}>"
