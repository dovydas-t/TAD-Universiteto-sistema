from app.extensions import db
from app.models.module import Module
from app.models.enum import SemesterEnum

class ModuleService:
    @staticmethod
    def get_all_modules():
        return Module.query.all()
    @staticmethod
    def get_module_by_id(module_id):
        return Module.query.get(module_id)
    @staticmethod
    def get_modules_by_study_program(study_program_id):
        return Module.query.filter_by(study_program_id=study_program_id).all()
    @staticmethod
    def create_module(name, description, credits, semester, study_program_id, image_path=None):
        if isinstance(semester, str):
            # Convert string to Enum if needed
            semester = SemesterEnum[semester]
        module = Module(
            name=name,
            description=description,
            credits=credits,
            semester=semester,
            study_program_id=study_program_id,
            image_path=image_path
        )
        db.session.add(module)
        db.session.commit()
        return module
    @staticmethod
    def update_module(module_id, **kwargs):
        module = get_module_by_id(module_id)
        if not module:
            return None
        for key, value in kwargs.items():
            if key == 'semester' and isinstance(value, str):
                value = SemesterEnum[value]
            setattr(module, key, value)
        db.session.commit()
        return module
    @staticmethod
    def delete_module(module_id):
        module = get_module_by_id(module_id)
        if not module:
            return False
        db.session.delete(module)
        db.session.commit()
        return True
