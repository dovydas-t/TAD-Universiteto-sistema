from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from app.forms.profile import ProfileForm
from app.extensions import db
from app.models.enum import RoleEnum
from app.utils.decorators import admin_required, teacher_status_required

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
    


# @bp.route('/admin_dashboard')
# @admin_required
# def admin_dashboard():


#     # total_students = UserProfile.query.filter_by(role=RoleEnum.Student).count()
#     # total_teachers = UserProfile.query.filter_by(role=RoleEnum.Teacher).count()
#     # study_programs = StudyProgram.query.all()
#     """                  total_students=total_students,
#                          total_teachers=total_teachers,
#                          study_programs=study_programs"""
#     return render_template('dashboard_base.html')

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


    

    
    
    
    