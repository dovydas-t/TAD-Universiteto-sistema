from app.models.study_program import StudyProgram
from app.extensions import db

class StudyProgramService:
    """Service class for study program operations"""

    @staticmethod
    def add_study_program(program: StudyProgram):
        db.session.add(program)
        db.session.commit()

    @staticmethod
    def get_all_study_programs():
        """Get all study programs"""
        return StudyProgram.query.all()

    @staticmethod
    def get_study_program_by_id(program_id):
        """Get a study program by its ID"""
        return StudyProgram.query.get(program_id)

    @staticmethod
    def create_study_program(name, description):
        """Create a new study program"""
        new_program = StudyProgram(name=name, description=description)
        db.session.add(new_program)
        db.session.commit()
        return new_program

    @staticmethod
    def update_study_program(program_id, name=None, description=None):
        """Update an existing study program"""
        program = StudyProgram.query.get(program_id)
        if not program:
            return None
        if name:
            program.name = name
        if description:
            program.description = description
        db.session.commit()
        return program

    @staticmethod
    def delete_study_program(program_id):
        """Delete a study program"""
        program = StudyProgram.query.get(program_id)
        if not program:
            return False
        db.session.delete(program)
        db.session.commit()
        return True
