# File: app/services/registration_service.py

from app.models.grade import Grade
from app.models.module_requirement import ModuleRequirement
from app.models.module import Module
from app.models.profile import UserProfile

class RegistrationDecisionEngine:
    """
    Simple service that decides whether registration should be immediate or require approval
    """
    
    def __init__(self):
        self.approval_reasons = []
    
    def evaluate_registration(self, student_id, study_program_id, module_id):
        """
        Main decision logic - returns ('immediate' or 'approval_required', [reasons])
        """
        self.approval_reasons = []
        
        # Only check the essential things
        prerequisites_ok = self._check_prerequisites(student_id, module_id)
        student_active = self._check_student_active(student_id)
        not_already_enrolled = self._check_not_already_enrolled(student_id, module_id)
        
        # Simple decision: ALL must be OK for immediate registration
        if prerequisites_ok and student_active and not_already_enrolled:
            return 'immediate', None
        else:
            return 'approval_required', self.approval_reasons
    
    def _check_prerequisites(self, student_id, module_id):
        """Check if student completed required modules"""
        try:
            # Get student's completed modules (grades >= 50)
            completed_grades = Grade.query.filter(
                Grade.student_id == student_id,
                Grade.grade.isnot(None),
                Grade.grade >= 50.0
            ).all()
            completed_module_ids = [grade.module_id for grade in completed_grades]
            
            # Get required modules
            requirements = ModuleRequirement.query.filter_by(module_id=module_id).all()
            required_module_ids = [req.required_module_id for req in requirements]
            
            # Check if missing any prerequisites
            missing = set(required_module_ids) - set(completed_module_ids)
            
            if missing:
                missing_modules = Module.query.filter(Module.id.in_(missing)).all()
                missing_names = [mod.name for mod in missing_modules]
                self.approval_reasons.append(f"Missing prerequisites: {', '.join(missing_names)}")
                return False
            
            return True
            
        except Exception:
            self.approval_reasons.append("Error checking prerequisites")
            return False
    
    def _check_student_active(self, student_id):
        """Check if student account is active"""
        try:
            student = UserProfile.query.get(student_id)
            
            if not student:
                self.approval_reasons.append("Student not found")
                return False
            
            if not student.is_active:
                self.approval_reasons.append("Student account is inactive")
                return False
            
            return True
            
        except Exception:
            self.approval_reasons.append("Error checking student status")
            return False
    
    def _check_not_already_enrolled(self, student_id, module_id):
        """Check if student is not already enrolled in this module"""
        try:
            # Check if already has grade entry for this module
            existing = Grade.query.filter_by(
                student_id=student_id,
                module_id=module_id
            ).first()
            
            if existing:
                if existing.grade is None:
                    self.approval_reasons.append("Already enrolled in this module")
                else:
                    self.approval_reasons.append("Already completed this module")
                return False
            
            return True
            
        except Exception:
            self.approval_reasons.append("Error checking enrollment status")
            return False


class RegistrationProcessor:
    """
    Simple service to handle registration
    """
    
    @staticmethod
    def process_immediate_registration(student_id, study_program_id, module_id):
        """Process immediate registration - just the basics"""
        from app.extensions import db
        from datetime import datetime
        
        try:
            student = UserProfile.query.get(student_id)
            
            # Update study program
            student.study_program_id = study_program_id
            student.updated_at = datetime.utcnow()
            
            # Create grade entry (NULL grade = enrolled)
            grade_entry = Grade(
                student_id=student_id,
                module_id=module_id,
                grade=None
            )
            db.session.add(grade_entry)
            
            # Simple group assignment
            RegistrationProcessor._assign_to_group(student_id, study_program_id)
            
            db.session.commit()
            return True
            
        except Exception as e:
            db.session.rollback()
            print(f"Registration failed: {str(e)}")
            return False
    
    @staticmethod
    def _assign_to_group(student_id, study_program_id):
        """Simple group assignment"""
        try:
            from app.models.groups import Groups
            student = UserProfile.query.get(student_id)
            
            # Find any group for this study program
            group = Groups.query.filter_by(study_program_id=study_program_id).first()
            if group:
                student.group_id = group.id
                
        except Exception:
            # Don't fail registration if group assignment fails
            pass


