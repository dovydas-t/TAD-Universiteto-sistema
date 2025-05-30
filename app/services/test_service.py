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
