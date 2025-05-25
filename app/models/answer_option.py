from app.extensions import db

class AnswerOption(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question_id = db.Column(db.Integer, db.ForeignKey('test_question.id'))
    option_text = db.Column(db.Text, nullable=False)
    is_correct = db.Column(db.Boolean, default=False)

    question = db.relationship("TestQuestion", back_populates="answer_options")
