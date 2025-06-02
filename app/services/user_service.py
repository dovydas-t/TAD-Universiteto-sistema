from app.models.profile import UserProfile
from app.models.enum import RoleEnum
from app.models.auth import AuthUser
from app.models.grade import Grade
from app.extensions import db
from datetime import datetime
from werkzeug.utils import secure_filename
import os
import uuid
import logging

logger = logging.getLogger(__name__)

class UserService:
    """Service class for user profile operations"""
    
    @staticmethod
    def check_email_exists(email: str) -> bool:
        """Check if email already exists in the database"""
        email = UserProfile.query.filter_by(email=email).first()
        if email:
            logger.info(f"Email {email} already exists.")
            return True

    @staticmethod
    def get_user_profile(user_id: int) -> UserProfile:
        """Get user profile by user ID"""
        try:
            return UserProfile.query.filter_by(id=user_id).first()
        except Exception as e:
            logger.error(f"Error getting user profile: {str(e)}")
            return None
        
    @staticmethod
    def get_all_teachers() -> UserProfile:
        """Get all teachers"""
        try:
            return UserProfile.query.filter_by(role=RoleEnum.Teacher).all()
        except Exception as e:
            logger.error(f"Error getting teachers: {str(e)}")
            return []
    
    @staticmethod
    def get_current_teacher_for_group(group_id):
        return UserProfile.query.filter_by(role=RoleEnum.Teacher, group_id=group_id).first()

    @staticmethod
    def get_students():
        return UserProfile.query.filter_by(role=RoleEnum.Student).all()
    
    @staticmethod
    def get_teacher_by_group(group_id):
        return UserProfile.query.filter_by(role=RoleEnum.Teacher, group_id=group_id).first()

    @staticmethod
    def get_students_by_group(group_id):
        return UserProfile.query.filter_by(role=RoleEnum.Student, group_id=group_id).all()

    @staticmethod
    def create_user_profile(user_id, profile_data: UserProfile):
        """Create user profile"""
        try:
            new_profile = UserProfile(
                user_id=user_id,
                first_name=profile_data.get('first_name'),
                last_name=profile_data.get('last_name'),
                phone=profile_data.get('phone'),
                date_of_birth=profile_data.get('date_of_birth'),
                address=profile_data.get('address'),
                bio=profile_data.get('bio'),
                created_at=datetime.utcnow()
            )
            
            db.session.add(new_profile)
            db.session.commit()
            
            logger.info(f"Profile created for user ID: {user_id}")
            return new_profile
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error creating user profile: {str(e)}")
            return None
    
    @staticmethod
    def update_user_profile(user_id, profile_data: UserProfile):
        """Update user profile"""
        try:
            profile = UserProfile.query.filter_by(user_id=user_id).first()
            
            if not profile:
                # Create profile if it doesn't exist
                return UserService.create_user_profile(user_id, profile_data)
            
            # Update existing profile
            profile.first_name = profile_data.get('first_name', profile.first_name)
            profile.last_name = profile_data.get('last_name', profile.last_name)
            profile.phone = profile_data.get('phone', profile.phone)
            profile.date_of_birth = profile_data.get('date_of_birth', profile.date_of_birth)
            profile.address = profile_data.get('address', profile.address)
            profile.bio = profile_data.get('bio', profile.bio)
            profile.updated_at = datetime.utcnow()
            
            db.session.commit()
            
            logger.info(f"Profile updated for user ID: {user_id}")
            return profile
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error updating user profile: {str(e)}")
            return None
    
    @staticmethod
    def upload_profile_picture(user_id, file):
        """Upload and save profile picture"""
        try:
            if not file or file.filename == '':
                return None
            
            # Check file extension
            allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
            if not ('.' in file.filename and 
                    file.filename.rsplit('.', 1)[1].lower() in allowed_extensions):
                return None
            
            # Generate unique filename
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4()}_{filename}"
            
            # Save file
            upload_folder = os.path.join('uploads', 'profile_pictures')
            os.makedirs(upload_folder, exist_ok=True)
            file_path = os.path.join(upload_folder, unique_filename)
            file.save(file_path)
            
            # Update profile
            profile = UserProfile.query.filter_by(user_id=user_id).first()
            if not profile:
                profile = UserProfile(user_id=user_id, created_at=datetime.utcnow())
                db.session.add(profile)
            
            profile.profile_picture = f"profile_pictures/{unique_filename}"
            profile.updated_at = datetime.utcnow()
            db.session.commit()
            
            logger.info(f"Profile picture uploaded for user ID: {user_id}")
            return profile.profile_picture
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error uploading profile picture: {str(e)}")
            return None
    
    @staticmethod
    def get_user_full_data(user_id):
        """Get complete user data including auth and profile"""
        try:
            user = AuthUser.query.get(user_id)
            if not user:
                return None
            
            profile = UserProfile.query.filter_by(user_id=user_id).first()
            
            return {
                'auth': user,
                'profile': profile,
                'full_name': f"{profile.first_name} {profile.last_name}" if profile else user.email
            }
            
        except Exception as e:
            logger.error(f"Error getting user full data: {str(e)}")
            return None
    
    @staticmethod
    def search_users(query, role=None):
        """Search users by name or email"""
        try:
            base_query = db.session.query(AuthUser, UserProfile).join(
                UserProfile, AuthUser.id == UserProfile.user_id, isouter=True
            ).filter(AuthUser.is_active == True)
            
            if role:
                base_query = base_query.filter(AuthUser.role == role)
            
            if query:
                search_filter = db.or_(
                    AuthUser.email.ilike(f'%{query}%'),
                    UserProfile.first_name.ilike(f'%{query}%'),
                    UserProfile.last_name.ilike(f'%{query}%')
                )
                base_query = base_query.filter(search_filter)
            
            return base_query.all()
            
        except Exception as e:
            logger.error(f"Error searching users: {str(e)}")
            return []

    @staticmethod
    def update_user_group_from_form(form, group_id):
        students = UserService.get_students()
        selected_student_ids = form.students.data
        selected_teacher_id = form.teacher_id.data

        # Assign students
        for student in students:
            student.group_id = group_id if student.id in selected_student_ids else None

        # Remove current teacher
        current_teacher = UserService.get_teacher_by_group(group_id)
        if current_teacher and (not selected_teacher_id or current_teacher.id != selected_teacher_id):
            current_teacher.group_id = None

        # Assign new teacher
        if selected_teacher_id:
            teacher = UserProfile.query.get(selected_teacher_id)
            if teacher and teacher.role.name == "Teacher":
                teacher.group_id = group_id

        db.session.commit()

    @staticmethod
    def get_student_and_student_grades(student_id):
        student = UserProfile.query.filter_by(id=student_id, role=RoleEnum.Student).first()
        if not student:
            return None, []

        grades = Grade.query.filter_by(student_id=student_id).all()
        return student, grades

    @staticmethod
    def update_student_info_from_form(student_id, form):
        student = UserService.get_user_profile(student_id)
        
        student.first_name = form.first_name.data
        student.last_name = form.last_name.data
        student.birth_date = form.birth_date.data
        student.email = form.email.data
        student.study_program_id = form.study_program_id.data
        student.group_id = form.group_id.data

        db.session.commit()
        return student
    
    @staticmethod
    def update_user_group(user_id, group_id):
        """Update user's group"""
        user_profile = UserService.get_user_profile(user_id)
        if user_profile:
            user_profile.group_id = group_id
            db.session.commit()
            return None
        return None