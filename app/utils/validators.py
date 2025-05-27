from wtforms.validators import ValidationError
from flask_login import current_user
from app.models.module_requirement import ModuleRequirement
from app.models.module import Module
from app.models.grade import Grade
from app.models.study_program import StudyProgram


import re


class StrongPassword:
    """Custom validator for strong passwords"""
    
    def __init__(self, message=None):
        if not message:
            message = 'Password must contain at least one uppercase letter, one lowercase letter, and one number.'
        self.message = message
    
    def __call__(self, form, field):
        password = field.data
        
        if not re.search(r'[A-Z]', password):
            raise ValidationError(self.message)
        if not re.search(r'[a-z]', password):
            raise ValidationError(self.message)
        if not re.search(r'\d', password):
            raise ValidationError(self.message)


class NoSpecialChars:
    """Validator to prevent special characters in usernames"""
    
    def __init__(self, message=None):
        if not message:
            message = 'Username can only contain letters, numbers, and underscores.'
        self.message = message
    
    def __call__(self, form, field):
        if not re.match(r'^[a-zA-Z0-9_]+$', field.data):
            raise ValidationError(self.message)

        

class ModuleRequirementsValidator:
    """
    Custom validator to check if student has completed prerequisite modules
    """
    
    def __init__(self, message=None, passing_grade=50.0):
        self.message = message
        self.passing_grade = passing_grade

    def __call__(self, form, field):
        selected_modules = field.data if field.data else []
        
        if not selected_modules:
            return
        
        # Get student's completed modules from Grade model
        student_profile_id = current_user.profile.id
        completed_grades = Grade.query.filter(
            Grade.student_id == student_profile_id,
            Grade.grade.isnot(None),
            Grade.grade >= self.passing_grade
        ).all()
        completed_module_ids = [grade.module_id for grade in completed_grades]
        
        # Handle both single module (SelectField) and multiple modules (SelectMultipleField)
        module_ids = selected_modules if isinstance(selected_modules, list) else [selected_modules]
        
        # Check each selected module for missing prerequisites
        for module_id in module_ids:
            self._validate_single_module(module_id, completed_module_ids)
    
    def _validate_single_module(self, module_id, completed_module_ids):
        """Validate prerequisites for a single module"""
        requirements = ModuleRequirement.query.filter_by(module_id=module_id).all()
        required_module_ids = [req.required_module_id for req in requirements]
        
        missing_prerequisites = set(required_module_ids) - set(completed_module_ids)
        
        if missing_prerequisites:
            current_module = Module.query.get(module_id)
            module_name = current_module.name if current_module else f"Module ID {module_id}"
            
            missing_modules = Module.query.filter(Module.id.in_(missing_prerequisites)).all()
            missing_names = [mod.name for mod in missing_modules]
            
            if self.message:
                error_message = self.message.format(
                    module_name=module_name,
                    missing_modules=', '.join(missing_names)
                )
            else:
                error_message = (
                    f"Cannot register for '{module_name}'. "
                    f"You must first complete: {', '.join(missing_names)}"
                )
            
            raise ValidationError(error_message)


class StudyProgramModulesValidator:
    """
    Validator to ensure selected modules belong to the chosen study program
    """
    
    def __init__(self, study_program_field='study_program_id', message=None):
        self.study_program_field = study_program_field
        self.message = message

    def __call__(self, form, field):
        study_program_field = getattr(form, self.study_program_field, None)
        
        if not study_program_field or not study_program_field.data or not field.data:
            return
        
        study_program_id = study_program_field.data
        selected_modules = field.data if isinstance(field.data, list) else [field.data]
        
        # Get valid modules for the selected study program
        valid_modules = Module.query.filter_by(study_program_id=study_program_id).all()
        valid_module_ids = [mod.id for mod in valid_modules]
        
        # Check if all selected modules are valid for this study program
        invalid_modules = set(selected_modules) - set(valid_module_ids)
        
        if invalid_modules:
            invalid_module_objects = Module.query.filter(Module.id.in_(invalid_modules)).all()
            invalid_names = [mod.name for mod in invalid_module_objects]
            
            if self.message:
                error_message = self.message.format(invalid_modules=', '.join(invalid_names))
            else:
                error_message = (
                    f"These modules don't belong to the selected study program: "
                    f"{', '.join(invalid_names)}"
                )
            
            raise ValidationError(error_message)


class StudyProgramRegistrationValidator:
    """
    Validator to check if student is already registered for a study program
    """
    
    def __init__(self, message=None, allow_change=False):
        self.message = message
        self.allow_change = allow_change

    def __call__(self, form, field):
        if not field.data:
            return
        
        # Check if study program exists
        study_program = StudyProgram.query.get(field.data)
        if not study_program:
            raise ValidationError("Selected study program does not exist.")
        
        # Check if student is already registered
        if hasattr(current_user, 'profile') and current_user.profile.study_program_id:
            if not self.allow_change and current_user.profile.study_program_id == field.data:
                if self.message:
                    error_message = self.message
                else:
                    error_message = "You are already registered for this study program."
                raise ValidationError(error_message)


class SemesterRequirementsValidator:
    """
    Validator to check if student meets minimum semester requirements for modules
    """
    
    def __init__(self, message=None, semester_field='current_semester'):
        self.message = message
        self.semester_field = semester_field

    def __call__(self, form, field):
        selected_modules = field.data if field.data else []
        selected_modules = selected_modules if isinstance(selected_modules, list) else [selected_modules]
        
        if not selected_modules:
            return
        
        # Get student's current semester
        student_semester = getattr(current_user.profile, self.semester_field, 1)
        
        for module_id in selected_modules:
            module = Module.query.get(module_id)
            
            if module and hasattr(module, 'min_semester'):
                if student_semester < module.min_semester:
                    if self.message:
                        error_message = self.message.format(
                            module_name=module.name,
                            min_semester=module.min_semester,
                            current_semester=student_semester
                        )
                    else:
                        error_message = (
                            f"Module '{module.name}' requires minimum semester {module.min_semester}. "
                            f"Your current semester: {student_semester}"
                        )
                    
                    raise ValidationError(error_message)


class EnrollmentLimitValidator:
    """
    Validator to check if student hasn't exceeded maximum module enrollment limit
    """
    
    def __init__(self, max_modules=5, message=None, include_current=True):
        self.max_modules = max_modules
        self.message = message
        self.include_current = include_current

    def __call__(self, form, field):
        selected_modules = field.data if field.data else []
        selected_modules = selected_modules if isinstance(selected_modules, list) else [selected_modules]
        
        if not selected_modules:
            return
        
        total_modules = len(selected_modules)
        
        if self.include_current:
            # Add currently enrolled modules (grades with NULL values)
            student_profile_id = current_user.profile.id
            enrolled_grades = Grade.query.filter(
                Grade.student_id == student_profile_id,
                Grade.grade.is_(None)
            ).all()
            total_modules += len(enrolled_grades)
        
        if total_modules > self.max_modules:
            if self.message:
                error_message = self.message.format(
                    total_modules=total_modules,
                    max_modules=self.max_modules
                )
            else:
                error_message = (
                    f"Cannot enroll in {total_modules} modules. "
                    f"Maximum allowed: {self.max_modules}"
                )
            
            raise ValidationError(error_message)
