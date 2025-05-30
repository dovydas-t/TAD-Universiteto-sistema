from app.extensions import db
from app.models.answer_option import AnswerOption

class AnswerOptionService:
    @staticmethod
    def create_answer_for_test_question_id(test_question_id: int, option_text: str, is_correct: bool) -> AnswerOption:
        answer = AnswerOption(
            question_id=test_question_id,
            option_text=option_text,
            is_correct=is_correct
        )
        db.session.add(answer)
        return answer