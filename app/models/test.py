from app.extensions import db

class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'))
    name = db.Column(db.String(255))

    module = db.relationship("Module", back_populates="tests")
    questions = db.relationship("TestQuestion", back_populates="test", cascade="all, delete-orphan")