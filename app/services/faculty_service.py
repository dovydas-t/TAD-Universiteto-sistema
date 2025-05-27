from app.extensions import db
from app.models import Faculty

class FacultyService:

    @staticmethod
    def add_faculty(faculty):
        db.session.add(faculty)
        db.session.commit()
        return faculty

    @staticmethod
    def get_all_faculties():
        return Faculty.query.all()

    @staticmethod
    def get_faculty_by_id(faculty_id):
        return Faculty.query.get(faculty_id)

    @staticmethod
    def update_faculty(faculty_id, name):
        faculty = Faculty.query.get(faculty_id)
        if faculty:
            faculty.name = name
            db.session.commit()
        return faculty

    @staticmethod
    def delete_faculty(faculty_id):
        faculty = Faculty.query.get(faculty_id)
        if faculty:
            db.session.delete(faculty)
            db.session.commit()
            return True
        return False
