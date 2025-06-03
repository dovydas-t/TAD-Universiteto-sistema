from flask import Blueprint, flash, request, redirect, render_template, url_for
from flask_login import login_required, current_user
from app.utils.decorators import admin_required
from app.services.module_service import ModuleService
from app.services.user_service import UserService
from collections import defaultdict

bp = Blueprint('grades', __name__)

@bp.route('/<int:student_id>', methods=['GET', 'POST'])
@login_required
def student_grades(student_id):
    student, grades = UserService.get_student_and_student_grades(student_id)

    if not student:
        flash("Error. Student don't exist.", 'error')
        return redirect(url_for('dashboard.index'))
    
    module_grade_map = defaultdict(list)
    for grade in grades:
        module = ModuleService.get_module_by_id(grade.module_id)
        module_grade_map[module.name].append(grade.grade)

    return render_template('grades/grades.html',
                           module_grade_map=module_grade_map)



@bp.route('/assign', methods=['POST'])
def assign():
    pass