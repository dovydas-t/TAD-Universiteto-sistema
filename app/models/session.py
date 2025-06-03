from app.extensions import db

class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'))
    type = db.Column(db.String(255))  # e.g., 'Lecture', 'Lab'
    date = db.Column(db.DateTime, nullable=False)

    module = db.relationship("Module", back_populates="sessions")