from flask import Blueprint, flash, request, redirect, render_template, url_for
from flask_login import login_required, current_user
from app.utils.decorators import admin_required

from app.models.study_program import StudyProgram
from app.services.study_program_service import StudyProgramService

from app.models.study_program import StudyProgram
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
                           study_program_list=study_program.id,  # Add this line
                           study_program= study_program,  # This was already here
                           faculty=faculty, 
                           modules=modules)

def list_programs():
    study_programs = StudyProgramService.get_all_study_programs()
    return render_template('programs/study_programs.html', study_programs=study_programs)


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