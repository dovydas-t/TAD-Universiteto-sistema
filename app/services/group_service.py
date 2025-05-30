from app.extensions import db, Optional
from app.models.groups import Groups
from app.models.enum import  RoleEnum
from app.models.profile import UserProfile


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
    def auto_assign_to_group(study_program_id: int) -> Optional[int]:
        """Auto-assign student to group with least members"""
        groups = Groups.query.filter_by(study_program_id=study_program_id).all()
        
        if not groups:
            return None
        
        # Find group with least members and available spots
        best_group = None
        min_count = float('inf')
        
        for group in groups:
            current_count = UserProfile.query.filter_by(
                group_id=group.id,
                role=RoleEnum.Student
            ).count()
            
            if current_count < group.max_capacity and current_count < min_count:
                min_count = current_count
                best_group = group
        
        return best_group.id if best_group else None
    
    @staticmethod
    def get_dropdown_choices():
        return [(g.id, g.code) for g in db.session.query(Groups).order_by(Groups.code).all()]
        