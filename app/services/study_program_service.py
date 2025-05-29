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
    
    @staticmethod
    def generate_group_code_for_study_program(study_program: StudyProgram, starting_year: int, existing_codes: list[str]) -> str:
        """Generate a group code like TAD-u-SP25-x for a study program, avoiding duplicates"""
        
        # Step 1: Generate program prefix
        print(f"DEBUG: study_program.name = {study_program.name}")

        words = study_program.name.split()
        code_prefix = ''.join(word[0].upper() for word in words if word)
        
        # Step 2: Year suffix
        year_suffix = str(starting_year)[-2:]
        
        # Step 3: Build base code (TAD-u-SP25)
        # T - Toma, A - Aivaras, D - Dovydas, u - university - XXX - Study Program name initials, 25 - last two digits of starting year
        base_code = f"TAD-u-{code_prefix}{year_suffix}"
        
        # Step 4: Find existing groups with same base
        existing_group_numbers = [
            int(code.rsplit('-', 1)[-1])
            for code in existing_codes
            if code.startswith(base_code + "-") and code.rsplit('-', 1)[-1].isdigit()
        ]
        
        # Step 5: Determine next group number
        next_group_number = max(existing_group_numbers, default=0) + 1
        
        return f"{base_code}-{next_group_number}"


    
