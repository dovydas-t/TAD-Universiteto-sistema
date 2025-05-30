from app.extensions import db
from app.models.test_question import TestQuestion
from app.models.answer_option import AnswerOption

class TestQuestionService:
    @staticmethod
    def get_all_test_questions():
        return TestQuestion.query.all()

    @staticmethod
    def get_test_question_by_id(test_id):
        question = TestQuestion.query.get(test_id)
        if question is None:
            raise ValueError(f"TestQuestion with id {test_id} not found.")
        return question
    
    @staticmethod
    def create_test_question(data):
        question = TestQuestion(**data)
        db.session.add(question)
        db.session.commit()
        return question
    
    @staticmethod
    def create_and_flush_question(test_id: int, question_text: str) -> TestQuestion:
        test_question = TestQuestion(test_id=test_id, question_text=question_text)
        db.session.add(test_question)
        db.session.flush()
        return test_question

    @staticmethod
    def delete_test_question(test_id):
        question = TestQuestion.query.get(test_id)
        if question:
            db.session.delete(question)
            db.session.commit()
            return True
        return False

    @staticmethod
    def create_test_question_from_form(form):
        correct_found = False
        answer_options = []

        for option_form in form.answer_options:
            text = option_form.option_text.data
            is_correct = option_form.is_correct.data
            if is_correct:
                correct_found = True
            answer_options.append(AnswerOption(text=text, is_correct=is_correct))

        if not correct_found:
            raise ValueError("At least one answer option must be marked as correct.")
            
        question = TestQuestion(
            test_id=form.test_id.data,
            question_text=form.question_text.data,
            answer_options=answer_options
        )

        db.session.add(question)
        db.session.commit()

        return question
    
    @staticmethod
    def commit_changes():
        db.session.commit()

    @staticmethod
    def update_test_question_from_form(question, form):
        question.question_text = form.question_text.data

        # Validate number of answer options
        if len(form.answer_options.entries) != len(question.answer_options):
            raise ValueError("Mismatch between existing and submitted answer options.")

        for i, answer_form in enumerate(form.answer_options.entries):
            option = question.answer_options[i]
            option.option_text = answer_form.option_text.data
            option.is_correct = answer_form.is_correct.data

        db.session.commit()