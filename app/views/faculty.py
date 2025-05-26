from flask import Blueprint, request, redirect, render_template
from flask_login import login_required, current_user
from app.services.study_program_service import StudyProgramService
from app.models.faculty import Faculty
from app.services.faculty_service import FacultyService


bp = Blueprint('faculty', __name__)

@bp.route('/')
def index():
    study_programs_list = StudyProgramService.get_all_study_programs() or []
    faculty_list = FacultyService.get_all_faculties() or []
    faculty_names = [faculty.name for faculty in faculty_list]

    if not faculty_list:
        return render_template('faculty/no_faculty.html',
                               title='No Faculties Available')
    
    return render_template('faculty/faculties.html',
                           title='TAD University Faculties',
                           study_programs_list=study_programs_list,
                           faculty_names=faculty_names)

@bp.route('/detail/<int:faculty_id>')
def detail(faculty_id):
    faculty = FacultyService.get_faculty_by_id(faculty_id) or []

    if not faculty:
        return render_template('faculty/no_faculty.html',
                               title='Faculty Not Found')
        
    return render_template('faculty/faculty_detail.html',
                           title='Faculty Detail',
                           study_programs_list = faculty.programs,
                           faculty=faculty)
