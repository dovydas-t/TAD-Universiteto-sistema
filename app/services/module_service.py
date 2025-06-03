from app.extensions import db
from app.models.module import Module
from app.models.module_requirement import ModuleRequirement
from app.models.enum import SemesterEnum

class ModuleService:
    @staticmethod
    def get_all_modules():
        return Module.query.all()
    
    @staticmethod
    def get_module_by_id(module_id):
        return Module.query.get(module_id)
    
    @staticmethod
    def get_modules_by_study_program_id(study_program_id):
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
        module = ModuleService.get_module_by_id(module_id)
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
        module = ModuleService.get_module_by_id(module_id)
        if not module:
            return False
        db.session.delete(module)
        db.session.commit()
        return True

    @staticmethod
    def create_module_from_form(form):
        # Handle optional image_path safely
        image_path = None
        if hasattr(form, 'image_path') and form.image_path.data:
            image_path = form.image_path.data  # Could be string or FileStorage, adjust as needed

        return ModuleService.create_module(
            name=form.name.data,
            description=form.description.data,
            credits=form.credits.data,
            semester=form.semester.data,
            study_program_id=form.study_program_id.data,
            image_path=image_path
        )
    @staticmethod
    def add_prerequisite(module_id, required_module_id):
        req = ModuleRequirement(module_id=module_id, required_module_id=required_module_id)
        db.session.add(req)
        db.session.commit()

    @staticmethod
    def get_all_modules_except(module_id):
        """Get all modules except the one with the given ID."""
        return Module.query.filter(Module.id != module_id).all()