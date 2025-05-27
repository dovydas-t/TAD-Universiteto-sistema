from flask import render_template, redirect, url_for, flash, Blueprint
from flask_login import login_required, current_user
from app.extensions import db
from app.forms.admin_approval_form import AdminApprovalForm
from app.models.registration_request import RegistrationRequest
from app.models.grade import Grade
from datetime import datetime

# Create blueprint for admin routes
bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    """Decorator to ensure only admins can access"""
    from functools import wraps
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.profile.role != 'admin':
            flash('Access denied. Admin privileges required.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


@bp.route('/pending-requests')
@login_required
@admin_required
def pending_requests():
    """Show all pending registration requests"""
    requests = RegistrationRequest.query.filter_by(
        status='pending'
    ).order_by(RegistrationRequest.created_at.asc()).all()
    
    # Add urgency info
    for request in requests:
        days_old = (datetime.utcnow() - request.created_at).days
        request.is_urgent = days_old > 3
        request.days_old = days_old
    
    return render_template('admin/pending_requests.html', requests=requests)


@bp.route('/process-request/<int:request_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def process_request(request_id):
    """Process a specific registration request"""
    request = RegistrationRequest.query.get_or_404(request_id)
    
    if request.status != 'pending':
        flash('This request has already been processed.', 'warning')
        return redirect(url_for('admin.pending_requests'))
    
    form = AdminApprovalForm()
    form.request_id.data = request_id
    
    if form.validate_on_submit():
        try:
            decision = form.decision.data
            admin_notes = form.admin_notes.data
            
            # Update request
            request.status = decision
            request.admin_notes = admin_notes
            request.admin_id = current_user.profile.id
            request.processed_at = datetime.utcnow()
            
            if decision == 'approved':
                # Actually register the student
                success = process_approved_registration(request)
                
                if success:
                    flash('✅ Request approved and student registered!', 'success')
                else:
                    flash('⚠️ Request approved but registration failed.', 'warning')
            else:
                flash('❌ Request rejected.', 'info')
            
            db.session.commit()
            return redirect(url_for('admin.pending_requests'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error processing request: {str(e)}', 'error')
    
    return render_template('admin/process_request.html', 
                         form=form, 
                         request=request)


@bp.route('/quick-approve/<int:request_id>')
@login_required
@admin_required
def quick_approve(request_id):
    """Quick approve a request"""
    request = RegistrationRequest.query.get_or_404(request_id)
    
    if request.status != 'pending':
        flash('Request already processed.', 'warning')
        return redirect(url_for('admin.pending_requests'))
    
    try:
        request.status = 'approved'
        request.admin_id = current_user.profile.id
        request.processed_at = datetime.utcnow()
        request.admin_notes = 'Quick approval'
        
        # Register the student
        process_approved_registration(request)
        
        db.session.commit()
        flash('✅ Request quickly approved!', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'error')
    
    return redirect(url_for('admin.pending_requests'))


@bp.route('/quick-reject/<int:request_id>')
@login_required
@admin_required
def quick_reject(request_id):
    """Quick reject a request"""
    request = RegistrationRequest.query.get_or_404(request_id)
    
    if request.status != 'pending':
        flash('Request already processed.', 'warning')
        return redirect(url_for('admin.pending_requests'))
    
    try:
        request.status = 'rejected'
        request.admin_id = current_user.profile.id
        request.processed_at = datetime.utcnow()
        request.admin_notes = 'Quick rejection'
        
        db.session.commit()
        flash('❌ Request rejected.', 'info')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'error')
    
    return redirect(url_for('admin.pending_requests'))


@bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    """Admin dashboard with overview"""
    pending_count = RegistrationRequest.query.filter_by(status='pending').count()
    today_count = RegistrationRequest.query.filter(
        RegistrationRequest.created_at >= datetime.utcnow().date()
    ).count()
    
    # Get urgent requests (>3 days old)
    urgent_requests = RegistrationRequest.query.filter(
        RegistrationRequest.status == 'pending',
        RegistrationRequest.created_at < (datetime.utcnow() - datetime.timedelta(days=3))
    ).all()
    
    return render_template('admin/dashboard.html',
                         pending_count=pending_count,
                         today_count=today_count,
                         urgent_count=len(urgent_requests),
                         urgent_requests=urgent_requests)


def process_approved_registration(request):
    """Actually register the student when approved"""
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
        
        return True
        
    except Exception as e:
        print(f"Error processing approved registration: {str(e)}")
        return False