from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from app.extensions import db
from app.forms.profile import ProfileForm
from app.forms.session_form import SessionForm
from app.models.enum import RoleEnum
from app.models.module import Module
from app.models.session import Session


from app.utils.decorators import admin_required, teacher_status_required, admin_or_teacher_role_required

bp = Blueprint('main', __name__)


@bp.route('/')
@bp.route('/index')
def index():
    """Home page"""
    return render_template('index.html', title='Home')

@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """User profile page"""    
    return render_template('profile.html', title='Profile')

@bp.route('/profile/update', methods=['GET', 'POST'])
@login_required
def profile_update():
    """User profile update"""
    form = ProfileForm(obj=current_user.profile)    
    if form.validate_on_submit():
        #TODO: Cia galbut reiketu sukurti papildomas funkcijas, kad kodas butu svaresnis
        # galbut galima butu panaudoti '__eq__' magic dunder
        user_changed = (
            form.username.data != current_user.username or
            form.first_name.data != current_user.profile.first_name or
            form.last_name.data != current_user.profile.last_name or
            form.email.data != current_user.profile.email or
            form.birth_date.data != current_user.profile.birth_date
        )

        if not user_changed:
            flash("No changes detected.", "info")
            return redirect(url_for('main.profile'))

        # Proceed with updating only if something changed
        current_user.username = form.username.data
        current_user.profile.first_name = form.first_name.data
        current_user.profile.last_name = form.last_name.data
        current_user.profile.email = form.email.data
        current_user.profile.birth_date = form.birth_date.data

        db.session.commit()
        flash("Profile updated successfully!", "success")
        return redirect(url_for('main.profile'))

    return render_template("profile/update_profile.html", form=form)

@bp.route('/dashboard')
@login_required
def dashboard():
    """User dashboard"""

    """User dashboard - redirects based on role"""
    try:
        if not current_user.profile:
            flash('Profile not found. Please contact administrator.', 'error')
            return redirect(url_for('auth.logout'))
        
        # Redirect based on user role
        # Redirect based on user role
        if current_user.profile.role == RoleEnum.Admin:
            return redirect(url_for('admin.admin_dashboard'))
        elif current_user.profile.role == RoleEnum.Teacher:
            return redirect(url_for('main.teacher_dashboard'))
        else:  # Default to student dashboard (no role check needed)
            return redirect(url_for('main.student_dashboard'))
    except Exception as e:
        print(f"{e}")
        return redirect(url_for('main.index'))


@bp.route('/teacher/dashboard')
@teacher_status_required
def teacher_dashboard():
    """Teacher dashboard"""
    teacher_profile = current_user.profile
    return render_template('teacher/dashboard.html', teacher=teacher_profile)

@bp.route('/student/dashboard')
@login_required  # Only login required, not role-specific
def student_dashboard():
    """Student dashboard - default for all users"""
    student_profile = current_user.profile
    study_program = student_profile.study_program if student_profile.study_program_id else None
    
    return render_template('student/dashboard.html', 
                         student=student_profile,
                         study_program=study_program)




@bp.route('/add_session', methods=['GET', 'POST'])
@admin_or_teacher_role_required
def add_session():
    try:
        form = SessionForm()
        form.module_id.choices = [(m.id, m.name) for m in Module.query.all()]
        if form.validate_on_submit():
            session = Session(
                module_id=form.module_id.data,
                type=form.type.data,
                date=form.date.data
            )
            db.session.add(session)
            db.session.commit()
            flash('Session added!', 'success')
            return redirect(url_for('main.add_session'))
        return render_template('session/add_session.html', form=form)
    except Exception as e:
        print(f"{e}")
        db.session.rollback()


@bp.route('/privacy')
def privacy():
    return render_template('admin/privacy.html')

@bp.route('/accessibility')
def accessibility():
    return render_template('admin/accessibility.html')

@bp.route('/media')
def media():
    return render_template('admin/media.html')