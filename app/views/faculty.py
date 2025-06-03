from flask import Blueprint, flash, request, redirect, render_template, url_for
from flask_login import login_required, current_user
from app.services.study_program_service import StudyProgramService
from app.models.faculty import Faculty
from app.services.faculty_service import FacultyService
from app.utils.decorators import admin_required
from app.forms.faculty import FacultyForm


bp = Blueprint('faculty', __name__)

@bp.route('/')
def index():
    faculty_list = FacultyService.get_all_faculties() or []
    faculty_names = [faculty.name for faculty in faculty_list]

    if not faculty_list:
        return render_template('faculty/no_faculty.html',
                               title='No Faculties Available')
    
    return render_template('faculty/faculties_list.html',
                           title='TAD University Faculties',
                           faculty_list=faculty_list,
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

@bp.route('/add_faculty', methods=['GET', 'POST'])
@admin_required
def add_faculty():
    """Add a new faculty"""
    form = FacultyForm()
    if form.validate_on_submit(): 
        new_faculty = Faculty(
            name=form.name.data,
            city=form.city.data,
            street=form.street.data,
            address=form.address.data,
            description=form.description.data)
        FacultyService.add_faculty(new_faculty)
        flash('Faculty added successfully!', 'success')
        return redirect(url_for('faculty.detail', faculty_id=new_faculty.id))
    
    if request.method == 'GET':
        return render_template('faculty/add_faculty.html', form=form, title='Add Faculty')