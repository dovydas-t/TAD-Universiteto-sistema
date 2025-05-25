from app.extensions import db

class TestQuestion(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    test_id = db.Column(db.Integer, db.ForeignKey('test.id'))
    question_text = db.Column(db.Text, nullable=False)

    test = db.relationship("Test", back_populates="questions")
    answer_options = db.relationship("AnswerOption", back_populates="question", cascade="all, delete-orphan")