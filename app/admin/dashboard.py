from flask_admin import AdminIndexView, expose
from flask_login import current_user
from flask import redirect, url_for
from datetime import datetime, timedelta
from app.models.registration_request import RegistrationRequest

class AdminDashboardView(AdminIndexView):
    """
    Custom admin dashboard with statistics
    """
    
    @expose('/')
    def index(self):
        """Main dashboard view"""
        
        # Statistics
        pending_count = RegistrationRequest.query.filter_by(status='pending').count()
        approved_count = RegistrationRequest.query.filter_by(status='approved').count()
        rejected_count = RegistrationRequest.query.filter_by(status='rejected').count()
        
        # Urgent requests (>3 days old)
        urgent_date = datetime.utcnow() - timedelta(days=3)
        urgent_requests = RegistrationRequest.query.filter(
            RegistrationRequest.status == 'pending',
            RegistrationRequest.created_at < urgent_date
        ).limit(5).all()
        
        # Recent activity
        recent_requests = RegistrationRequest.query.order_by(
            RegistrationRequest.created_at.desc()
        ).limit(10).all()
        
        return self.render('admin/dashboard.html',
                         pending_count=pending_count,
                         approved_count=approved_count,
                         rejected_count=rejected_count,
                         urgent_requests=urgent_requests,
                         recent_requests=recent_requests)
    
    def is_accessible(self):
        return current_user.is_authenticated and current_user.profile.role == 'admin'
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login'))
