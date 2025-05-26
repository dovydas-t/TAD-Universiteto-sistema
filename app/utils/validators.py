from wtforms.validators import ValidationError
from flask_login import current_user
from app.models.module_requirement import ModuleRequirement
from app.models.module import Module
from app.models.grade import Grade

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
    Custom validator class to check if student has completed prerequisite modules
    before allowing registration for higher-level modules.
    """
    
    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        """
        Main validation method called by WTForms
        """
        selected_modules = field.data if field.data else []
        
        if not selected_modules:
            return
        
        # Get student's completed modules
        completed_module_ids = self._get_student_completed_modules()
        
        # Check each selected module for missing prerequisites
        for module_id in selected_modules:
            self._validate_single_module(module_id, completed_module_ids)
    
    def _get_student_completed_modules(self):
        """
        Get list of module IDs that the current student has completed.
        Uses the Grade model to determine completed modules.
        """
        student_id = current_user.id
        
        # Get completed modules based on grades
        # Adjust the grade threshold and field names based on your Grade model
        completed_grades = Grade.query.filter(
            Grade.student_id == student_id,
            Grade.grade.isnot(None),  # Has received a grade
            Grade.grade >= 50  # Assuming 50+ is passing grade - adjust as needed
        ).all()
        
        return [grade.module_id for grade in completed_grades]
        
        # Alternative approach if your Grade model has a different structure:
        # completed_grades = Grade.query.filter(
        #     Grade.user_id == student_id,  # if you use user_id instead
        #     Grade.status == 'passed'  # if you have a status field
        # ).all()
        # return [grade.module_id for grade in completed_grades]
    
    def _validate_single_module(self, module_id, completed_module_ids):
        """
        Validate prerequisites for a single module
        """
        # Get module requirements
        requirements = ModuleRequirement.query.filter_by(module_id=module_id).all()
        required_module_ids = [req.required_module_id for req in requirements]
        
        # Check if student has completed all required prerequisite modules
        missing_prerequisites = set(required_module_ids) - set(completed_module_ids)
        
        if missing_prerequisites:
            # Get module names for error message
            current_module = Module.query.get(module_id)
            module_name = current_module.name if current_module else f"Module ID {module_id}"
            
            missing_modules = Module.query.filter(Module.id.in_(missing_prerequisites)).all()
            missing_names = [mod.name for mod in missing_modules]
            
            # Use custom message if provided, otherwise use default
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
