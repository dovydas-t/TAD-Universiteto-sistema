from app.extensions import db

class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'))
    title = db.Column(db.String(255))
    due_date = db.Column(db.DateTime)

    module = db.relationship("Module", back_populates="assignments")
