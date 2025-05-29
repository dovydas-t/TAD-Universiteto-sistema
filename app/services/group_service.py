from app.extensions import db
from app.models.groups import Groups

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
            code=code
        )
        db.session.add(group)
        db.session.commit()
        return group
    
        