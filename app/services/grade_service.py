from app.extensions import db
from datetime import datetime
from app.models.grade import Grade
from app.services.user_service import UserService
from app.services.test_service import TestService

class GradeService:
    @staticmethod
    def add_grade_for_student(student_id: int, test_id: int, grade: float):
        """Add a grade for a student for a specific test."""
        student = UserService.get_user_profile(student_id)
        grades = student.grades if student else None
        if not student:
            raise ValueError("Student not found")
        
        test = TestService.get_test_by_id(test_id)
        if not test:
            raise ValueError("Test not found")
        
        module_id = test.module_id
        if not module_id:
            raise ValueError("Test does not belong to any module")
        
        new_grade = Grade(
            student_id=student.id,
            module_id=module_id,
            grade=grade
        )
        db.session.add(new_grade)
        db.session.commit()
        