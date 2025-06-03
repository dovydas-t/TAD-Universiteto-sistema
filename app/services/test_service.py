from app.extensions import db
from app.models.test import Test

class TestService:
    @staticmethod
    def get_all_tests():
        return Test.query.all()

    @staticmethod
    def get_test_by_id(test_id):
        return Test.query.get(test_id)

    @staticmethod
    def create_test(data):
        new_test = Test(**data)
        db.session.add(new_test)
        db.session.commit()
        return new_test

    @staticmethod
    def update_test(test_id, data):
        test = Test.query.get(test_id)
        if not test:
            return None
        for key, value in data.items():
            setattr(test, key, value)
        db.session.commit()
        return test

    @staticmethod
    def delete_test(test_id):
        test = Test.query.get(test_id)
        if not test:
            return False
        db.session.delete(test)
        db.session.commit()
        return True

    @staticmethod
    def calculate_grade(correct_count: int, total_questions: int) -> float:
        if total_questions == 0:
            return 0.0
        # Simple percentage score (0 to 100)
        score_percent = (correct_count / total_questions) * 100

        # Optional: Convert to 0-10 scale
        grade = round(score_percent / 10, 2)  # e.g. 85% -> 8.5

        return grade
