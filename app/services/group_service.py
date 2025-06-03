from app.extensions import db, Optional
from app.models.groups import Groups
from app.models.enum import  RoleEnum
from app.models.profile import UserProfile
from datetime import datetime
from app.services.study_program_service import StudyProgramService
from app.services.user_service import UserService

class GroupsService:
    """Service class for module operations"""
    @staticmethod
    def get_all_groups():
        """Get all groups"""
        return Groups.query.all()
    
    @staticmethod
    def get_group_by_id(group_id):
        """Get group by id"""
        return Groups.query.filter_by(id=group_id).first()
    
    @staticmethod
    def get_group_codes_by_study_program_id(study_program_id):
        """Get all group codes for a specific study program"""
        return [group.code for group in Groups.query.filter_by(study_program_id=study_program_id).all()]
    
    @staticmethod
    def get_groups_by_study_program_id(study_program_id):
        """Get all groups for a specific study program"""
        return Groups.query.filter_by(study_program_id=study_program_id).all()

    @staticmethod
    def create_group_from_form(form, code):
        """Create a new group from a form"""
        group = Groups(
            study_program_id=form.study_program_id.data,
            max_capacity = form.max_capacity.data,
            code=code
        )
        db.session.add(group)
        db.session.commit()
        return group
    
    @staticmethod
    def create_group_for_study_program(study_program_id: int) -> Groups: #Groups is 1 object
        """Create a new group for a specific study program"""
        current_year = datetime.now().year
        existing_group_codes = GroupsService.get_group_codes_by_study_program_id(study_program_id)
        study_program = StudyProgramService.get_study_program_by_id(study_program_id)
        code = StudyProgramService.generate_group_code_for_study_program(study_program, current_year, existing_group_codes)

        group = Groups(
            study_program=study_program,
            max_capacity=10,  # Default capacity, can be adjusted
            code=code
        )
        db.session.add(group)
        db.session.commit()
        return group

    @staticmethod
    def auto_assign_to_group(study_program_id: int):
        """Auto-assign student to a group; create new group if none exist or all are full."""
        existing_groups = GroupsService.get_groups_by_study_program_id(study_program_id)
        
        if not existing_groups:
            # No groups exist, create the first one
            new_group = GroupsService.create_group_for_study_program(study_program_id)
            return new_group.id

        # Try to find a group with available capacity
        for group in existing_groups:
            students = UserService.get_students_by_group(group.id)
            if len(students) < group.max_capacity:
                return group.id

        # All groups are full, create a new one
        new_group = GroupsService.create_group_for_study_program(study_program_id)
        return new_group.id

    
    @staticmethod
    def get_dropdown_choices():
        return [(g.id, g.code) for g in db.session.query(Groups).order_by(Groups.code).all()]
        
    @staticmethod
    def delete_group(group_id: int):
        """Delete a group by its ID"""
        group = GroupsService.get_group_by_id(group_id)
        if not group:
            return False
        
        db.session.delete(group)
        db.session.commit()