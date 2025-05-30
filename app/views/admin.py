from flask import Blueprint, flash, request, redirect, render_template, url_for
from flask_login import login_required, current_user
from app.utils.decorators import admin_required

from app.models.profile import UserProfile
from app.services.user_service import UserService

from app.models.faculty import Faculty
from app.services.faculty_service import FacultyService
from app.forms.faculty import FacultyForm

from app.models.module import Module
from app.services.module_service import ModuleService

from app.models.study_program import StudyProgram
from app.services.study_program_service import StudyProgramService

from app.models.groups import Groups
# from app.services.groups_service import GroupsService

from app.models.grade import Grade
# from app.services.grade_service import GradeService

from app.models.module_requirement import ModuleRequirement
# from app.services.module_requirement_service import ModuleRequirementService

from app.models.assignment import Assignment
# from app.services.assignment_service import AssignmentService

from app.models.schedule_item import ScheduleItem
# from app.services.schedule_item_service import ScheduleItemService

from app.models.test import Test
# from app.services.test_service import TestService

from app.models.test_question import TestQuestion
# from app.services.test_question_service import TestQuestionService

from app.models.answer_option import AnswerOption
# from app.services.answer_option_service import AnswerOptionService

from app.models.attendance import Attendance
# from app.services.attendance_service import AttendanceService



bp = Blueprint('admin', __name__)


@bp.route('/dashboard', methods=['GET'])
@admin_required
def admin_dashboard():
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

@bp.route('/menu')
@admin_required
def menu():
    """Admin menu"""
    return render_template('admin/dashboard.html', title='Admin')
