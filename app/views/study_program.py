from flask import Blueprint, flash, request, redirect, render_template, url_for
from app.extensions import db, datetime
from flask import Blueprint, request, redirect, render_template,flash,url_for
from flask_login import login_required, current_user
from app.utils.decorators import admin_required

from app.models.study_program import StudyProgram
from app.services.study_program_service import StudyProgramService

from app.forms.hybrid_registration_form import HybridRegistrationForm
from app.models.study_program import StudyProgram
from app.models.module import Module
from app.models.grade import Grade
from app.services.faculty_service import FacultyService

from app.forms.study_program import StudyProgramForm
from app.services.module_service import ModuleService

bp = Blueprint('programs', __name__)

@bp.route('/')
def index():
    study_programs_list = StudyProgramService.get_all_study_programs() or []
    faculty_list = FacultyService.get_all_faculties() or []
    faculty_names = [faculty.name for faculty in faculty_list]

    if not study_programs_list:
        return render_template('programs/no_programs.html',
                               title='No Study Programs Available')
    
    return render_template('programs/study_programs.html',
                           title='Study Programs',
                           study_programs_list=study_programs_list,
                           faculty_names=faculty_names)


@bp.route('/detail/<int:study_program_id>')
def detail(study_program_id):
    study_program = StudyProgramService.get_study_program_by_id(study_program_id)
    
    if not study_program:
        return render_template('programs/no_program.html',
                               title='Study Program Not Found')
    
    faculty = FacultyService.get_faculty_by_id(study_program.faculty_id)
    modules = ModuleService.get_modules_by_study_program_id(study_program_id) or []
    
    return render_template('programs/study_program_detail.html',
                           title='Study Program Detail',
                           study_program=study_program,
                           faculty=faculty, 
                           modules=modules)

bp.route('/registration_to_study_program', methods=['GET', 'POST'])
@login_required
def register_study_program():
    """
    Handle study program and module registration for students
    """
    form = HybridRegistrationForm()
    
    if form.validate_on_submit():
        try:
            # Extract data from the form
            study_program_id = form.study_program_id.data
            selected_module_ids = form.module_id.data
            auth_user_id = current_user.id
            student_profile_id = current_user.profile.id
            
            # Validate that study program exists
            study_program = StudyProgram.query.get(study_program_id)
            if not study_program:
                flash('Selected study program not found.', 'error')
                return render_template('registration/study_program.html', form=form)
            
            # Check if student is already registered for this study program
            if current_user.profile.study_program_id == study_program_id:
                flash('You are already registered for this study program.', 'warning')
                return render_template('registration/study_program.html', form=form)
            
            # Process the registration
            success = process_registration(student_profile_id, study_program_id, selected_module_ids)
            
            if success:
                # Success messages
                flash(f'Successfully registered for {study_program.name}!', 'success')
                flash(f'Enrolled in {len(selected_module_ids)} modules.', 'info')
                
                # Show enrolled module names
                module_names = []
                for module_id in selected_module_ids:
                    module = Module.query.get(module_id)
                    if module:
                        module_names.append(module.name)
                
                if module_names:
                    flash(f'Modules: {", ".join(module_names)}', 'info')
                
                return redirect(url_for('dashboard.index'))  # Adjust redirect as needed
            else:
                flash('Registration failed. Please try again.', 'error')
                
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred during registration: {str(e)}', 'error')
            print(f"Registration error: {str(e)}")  # For debugging
    
    else:
        # Form validation failed - errors will be displayed in template
        if form.errors:
            flash('Please correct the errors below.', 'warning')
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f'{field}: {error}', 'error')
    
    return render_template('registration/study_program.html', form=form)


def process_registration(student_profile_id, study_program_id, selected_module_ids):
    """
    Process the actual registration logic using existing database tables
    """
    try:
        # Update study program in user_profile table
        current_user.profile.study_program_id = study_program_id
        current_user.profile.updated_at = datetime.utcnow()
        
        # Create grade placeholders for module enrollment tracking
        # This uses your existing grade table without needing new tables
        for module_id in selected_module_ids:
            # Check if grade entry already exists
            existing_grade = Grade.query.filter_by(
                student_id=student_profile_id,
                module_id=module_id
            ).first()
            
            if not existing_grade:
                # Create new grade entry with NULL grade (indicates enrollment)
                grade_entry = Grade(
                    student_id=student_profile_id,
                    module_id=module_id,
                    grade=None  # Will be filled when student is actually graded
                )
                db.session.add(grade_entry)
                print(f"Enrolled student {student_profile_id} in module {module_id}")
            else:
                print(f"Student {student_profile_id} already has entry for module {module_id}")
        
        # Commit all changes to MySQL database
        db.session.commit()
        print(f"Successfully registered student {student_profile_id} for program {study_program_id}")
        return True
        
    except Exception as e:
        # Rollback on any error
        db.session.rollback()
        print(f"Registration failed: {str(e)}")
        return False

@bp.route('/add_program', methods=['GET', 'POST'])
@admin_required
def add_program():
    """Add a new study program"""
    form = StudyProgramForm()
    
    if form.validate_on_submit():
        new_program = StudyProgram(
            name=form.name.data,
            faculty_id=form.faculty_id.data
        )
        StudyProgramService.add_study_program(new_program)
        flash('Study Program added successfully!', 'success')
        return redirect(url_for('programs.detail', study_program_id=new_program.id))
    
    if request.method == 'GET':
        return render_template('programs/add_program.html', form=form, title='Add Study Program')