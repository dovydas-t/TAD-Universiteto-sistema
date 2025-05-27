from flask import flash
from flask_login import current_user
from flask_admin.actions import action

from datetime import datetime
from app.extensions import db
from app.models.registration_request import RegistrationRequest
class BulkActions:
    """
    Bulk actions for admin interface
    """
    
    @action('approve_selected', 'Approve Selected', 'Are you sure you want to approve selected requests?')
    def approve_selected(self, ids):
        """Bulk approve multiple requests"""
        try:
            count = 0
            for request_id in ids:
                request = RegistrationRequest.query.get(request_id)
                if request and request.status == 'pending':
                    request.status = 'approved'
                    request.admin_id = current_user.profile.id
                    request.processed_at = datetime.utcnow()
                    request.admin_notes = 'Bulk approval'
                    count += 1
            
            db.session.commit()
            flash(f'Successfully approved {count} requests.', 'success')
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error in bulk approval: {str(e)}', 'error')
    
    @action('reject_selected', 'Reject Selected', 'Are you sure you want to reject selected requests?')
    def reject_selected(self, ids):
        """Bulk reject multiple requests"""
        try:
            count = 0
            for request_id in ids:
                request = RegistrationRequest.query.get(request_id)
                if request and request.status == 'pending':
                    request.status = 'rejected'
                    request.admin_id = current_user.profile.id
                    request.processed_at = datetime.utcnow()
                    request.admin_notes = 'Bulk rejection'
                    count += 1
            
            db.session.commit()
            flash(f'Successfully rejected {count} requests.', 'info')
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error in bulk rejection: {str(e)}', 'error')