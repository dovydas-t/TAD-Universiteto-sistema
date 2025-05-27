from flask import redirect, url_for, flash
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from flask_login import current_user
from datetime import datetime
from app.extensions import db
from app.models.registration_request import RegistrationRequest
from app.models.study_program import StudyProgram
from app.models.module import Module
from app.models.profile import UserProfile
from app.models.grade import Grade

class AdminRequiredMixin:
    """
    Mixin for admin access control
    """
    def is_accessible(self):
        return current_user.is_authenticated and current_user.profile.role == 'admin'
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login'))

class RegistrationRequestView(AdminRequiredMixin, ModelView):
    """
    Main view for managing registration requests
    """
    model = RegistrationRequest
    
    # Display configuration
    column_list = [
        'id', 'student.first_name', 'student.last_name', 'student.email',
        'study_program.name', 'module.name', 'status', 'reason', 'created_at'
    ]
    
    column_labels = {
        'student.first_name': 'First Name',
        'student.last_name': 'Last Name', 
        'student.email': 'Email',
        'study_program.name': 'Study Program',
        'module.name': 'Module',
        'created_at': 'Requested Date'
    }
    
    column_searchable_list = ['student.first_name', 'student.last_name', 'student.email']
    column_filters = ['status', 'study_program.name', 'module.name', 'created_at']
    column_default_sort = ('created_at', True)
    
    # Form configuration
    form_columns = ['status', 'admin_notes']
    form_choices = {
        'status': [
            ('pending', 'Pending'),
            ('approved', 'Approved'), 
            ('rejected', 'Rejected')
        ]
    }
    
    # Custom formatting
    def _status_formatter(view, context, model, name):
        status = model.status
        if status == 'pending':
            return f'<span class="label label-warning">⏳ {status.title()}</span>'
        elif status == 'approved':
            return f'<span class="label label-success">✅ {status.title()}</span>'
        elif status == 'rejected':
            return f'<span class="label label-danger">❌ {status.title()}</span>'
        return status
    
    column_formatters = {
        'status': _status_formatter
    }
    
    def on_model_change(self, form, model, is_created):
        """Process approval/rejection"""
        if not is_created:
            model.admin_id = current_user.profile.id
            model.processed_at = datetime.utcnow()
            
            if model.status == 'approved':
                self._process_approval(model)
            
            flash(f'Request {model.id} has been {model.status}!', 'success')
    
    def _process_approval(self, request):
        """Actually register the student"""
        try:
            # Update study program
            request.student.study_program_id = request.study_program_id
            request.student.updated_at = datetime.utcnow()
            
            # Create grade entry
            existing_grade = Grade.query.filter_by(
                student_id=request.student_id,
                module_id=request.module_id
            ).first()
            
            if not existing_grade:
                grade_entry = Grade(
                    student_id=request.student_id,
                    module_id=request.module_id,
                    grade=None
                )
                db.session.add(grade_entry)
                
                # Group assignment
                self._assign_to_group(request.student, request.study_program_id)
            
        except Exception as e:
            flash(f'Registration error: {str(e)}', 'warning')
    
    def _assign_to_group(self, student, study_program_id):
        """Simple group assignment"""
        try:
            from app.models.groups import Groups
            group = Groups.query.filter_by(study_program_id=study_program_id).first()
            if group:
                student.group_id = group.id
        except Exception:
            pass
    
    def __init__(self, name=None, category=None, endpoint=None, url=None, **kwargs):
        super(RegistrationRequestView, self).__init__(
            self.model, db.session, name, category, endpoint, url, **kwargs
        )

class QuickActionsView(AdminRequiredMixin, BaseView):
    """
    Quick action buttons for common operations
    """
    
    @expose('/')
    def index(self):
        """Quick actions dashboard"""
        pending_requests = RegistrationRequest.query.filter_by(status='pending').all()
        return self.render('admin/quick_actions.html', requests=pending_requests)
    
    @expose('/approve/<int:request_id>')
    def quick_approve(self, request_id):
        """Quick approve action"""
        request = RegistrationRequest.query.get_or_404(request_id)
        
        if request.status != 'pending':
            flash('Request already processed.', 'warning')
        else:
            request.status = 'approved'
            request.admin_id = current_user.profile.id
            request.processed_at = datetime.utcnow()
            request.admin_notes = 'Quick approval'
            
            # Process approval
            view = RegistrationRequestView()
            view._process_approval(request)
            
            db.session.commit()
            flash(f'Request #{request_id} approved!', 'success')
        
        return redirect(url_for('.index'))
    
    @expose('/reject/<int:request_id>')
    def quick_reject(self, request_id):
        """Quick reject action"""
        request = RegistrationRequest.query.get_or_404(request_id)
        
        if request.status != 'pending':
            flash('Request already processed.', 'warning')
        else:
            request.status = 'rejected'
            request.admin_id = current_user.profile.id
            request.processed_at = datetime.utcnow()
            request.admin_notes = 'Quick rejection'
            
            db.session.commit()
            flash(f'Request #{request_id} rejected.', 'info')
        
        return redirect(url_for('.index'))

# Additional Model Views
class StudyProgramView(AdminRequiredMixin, ModelView):
    """Manage study programs"""
    model = StudyProgram
    column_list = ['id', 'name', 'faculty.name']
    column_labels = {'faculty.name': 'Faculty'}
    
    def __init__(self, name=None, **kwargs):
        super(StudyProgramView, self).__init__(
            self.model, db.session, name, **kwargs
        )

class ModuleView(AdminRequiredMixin, ModelView):
    """Manage modules"""
    model = Module
    column_list = ['id', 'name', 'credits', 'semester', 'study_program.name']
    column_labels = {'study_program.name': 'Study Program'}
    column_filters = ['study_program.name', 'semester']
    
    def __init__(self, name=None, **kwargs):
        super(ModuleView, self).__init__(
            self.model, db.session, name, **kwargs
        )

class UserView(AdminRequiredMixin, ModelView):
    """Manage users"""
    model = UserProfile
    column_list = ['id', 'first_name', 'last_name', 'email', 'role', 'is_active']
    column_filters = ['role', 'is_active', 'study_program.name']
    column_searchable_list = ['first_name', 'last_name', 'email']
    
    def __init__(self, name=None, **kwargs):
        super(UserView, self).__init__(
            self.model, db.session, name, **kwargs
        )
