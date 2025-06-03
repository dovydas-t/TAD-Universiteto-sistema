from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from app.models.enum import RoleEnum
from app.services.user_service import UserService
from app.services.study_program_service import StudyProgramService
from app.services.module_service import ModuleService
from app.services.faculty_service import FacultyService

from app.utils.decorators import admin_required, teacher_status_required

bp = Blueprint('dashboard', __name__)

@bp.route('/')
@login_required
def dashboard():
    """User dashboard"""

    """User dashboard - redirects based on role"""
    try:
        if not current_user.profile:
            flash('Profile not found. Please contact administrator.', 'error')
            return redirect(url_for('auth.logout'))
        
        # Redirect based on user role
        if current_user.profile.role == RoleEnum.Admin:
            return redirect(url_for('dashboard.admin_dashboard'))
        elif current_user.profile.role == RoleEnum.Teacher:
            return redirect(url_for('dashboard.teacher_dashboard'))
        else:  # Default to student dashboard (no role check needed)
            return redirect(url_for('dashboard.student_dashboard'))
    except Exception as e:
        print(f"{e}")
        return redirect(url_for('main.index'))

@bp.route('/admin', methods=['GET'])
@admin_required
def admin_dashboard():
    try:
        faculties = FacultyService.get_all_faculties()
        study_programs = StudyProgramService.get_all_study_programs()
        modules = ModuleService.get_all_modules()
        teachers = UserService.get_all_teachers()

        """Admin dashboard"""
        return render_template('admin/dashboard.html',
                            title='TAD University Modules',
                            faculties=faculties,
                            modules=modules,
                            study_programs=study_programs,
                            teachers=teachers)
    except Exception as e:
        print(f"{e}")
        return render_template('admin/dashboard.html',
                            title='TAD University Modules',
                            faculties=faculties,
                            modules=modules,
                            study_programs=study_programs,
                            teachers=teachers)

@bp.route('/teacher')
@teacher_status_required
def teacher_dashboard():
    """Teacher dashboard"""
    teacher_profile = current_user.profile
    return render_template('teacher/dashboard.html', teacher=teacher_profile)

@bp.route('/student')
@login_required  # Only login required, not role-specific
def student_dashboard():
    """Student dashboard - default for all users"""
    student_profile = current_user.profile
    study_program = student_profile.study_program if student_profile.study_program_id else None
    
    return render_template('student/dashboard.html', 
                         student=student_profile,
                         study_program=study_program)