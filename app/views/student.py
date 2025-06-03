from flask import render_template, redirect, url_for, flash, Blueprint
from flask_login import login_required, current_user
from app.extensions import db
from app.forms.student_form import StudentEditForm
from app.models.module import Module
from app.models.study_program import StudyProgram
from app.models.schedule_item import ScheduleItem
from app.models.profile import UserProfile
from app.models.enum import RoleEnum
from app.forms.choosemodule import ChooseModule
from app.services.user_service import UserService
from app.services.group_service import GroupsService
from app.services.schedule_service import ScheduleService





bp = Blueprint('student', __name__, url_prefix='/student')


@bp.route('/academic-info')
@login_required  # or @login_required if you don't have student_required decorator
def academic_info():
    """View student's academic information"""
    student = current_user.profile
    return render_template('student/academic_info.html', student=student)

@bp.route('/modules')
@login_required
def my_modules():
    """View all student's enrolled modules"""
    # Get modules through enrollment or group assignment
    # You'll need to adjust this based on how students are enrolled in modules
    modules = Module.query.join(StudyProgram)\
        .filter(StudyProgram.id == current_user.profile.study_program_id)\
        .order_by(Module.semester.asc()).all()
    
    # Group modules by semester
    modules_by_semester = {}
    for module in modules:
        semester = module.semester.value if module.semester else 'Unknown'
        if semester not in modules_by_semester:
            modules_by_semester[semester] = []
        modules_by_semester[semester].append(module)
    
    return render_template(
    'student/student_modules.html',
    modules_by_semester=modules_by_semester,
    student=current_user.profile)

@bp.route('/my_calendar')
@login_required
def my_calendar():
    # Get all schedule items for the current user, ordered by date
    schedule_items = ScheduleItem.query.filter_by(user_id=current_user.profile.id).order_by(ScheduleItem.date).all()
    return render_template('schedule/schedule.html', schedule_items=schedule_items)

@bp.route('/academic-info')
@login_required  # or @login_required if you don't have student_required decorator
def student_modules():
    return render_template()

@bp.route('/detail/<int:student_id>', methods=['GET', 'POST'])
@login_required
def detail(student_id):
    student = UserService.get_user_profile(student_id)

    if not student:
        flash(f'Error: No student at ID: {student_id}', 'error')
        return redirect(url_for('module.index'))

    # Example: Build a module-to-grade mapping
    module_grade_map = {}
    for grade in student.grades:
        module_grade_map[grade.module_id] = grade.value  # or grade.grade, depending on your model

    return render_template(
        'student/student_detail.html',
        title='Student Details',
        student_id=student.id,
        student=student,
        module_grade_map=module_grade_map
    )


@bp.route('/edit/<int:student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    # print(f"Received student_id: {student_id} ({type(student_id)})")
    student = UserService.get_user_profile(student_id)
    print("Student found:", student)


    if student is None:
        flash("Student don't exist", 'error')
        redirect(url_for('main.index'))

    form = StudentEditForm(obj=student)

    if form.validate_on_submit():
        UserService.update_student_info_from_form(student_id, form)
        flash('Student profile updated successfully.', 'success')
        return redirect(url_for('main.index'))

    return render_template('student/edit_student.html', form=form, student=student)

@bp.route('/group-info')
@login_required
def group_info():
    """View group information"""
    
    if not current_user.profile.group_id:
        flash('You are not assigned to any group.', 'info')
        return redirect(url_for('dashboard.student_dashboard'))
    
    group_id = current_user.profile.group_id
    group = GroupsService.get_group_by_id(group_id)
    # Get all students in this group
    group_members = UserProfile.query.filter_by(
        group_id=group_id,
        role=RoleEnum.Student
    ).all()
    
    return render_template('groups/groups_info.html',
                         group=group,
                         group_members=group_members)



@bp.route('/choose_module', methods=['GET', 'POST'])
@login_required
def choose_module():
    try:
        form = ChooseModule()
        
        study_program_id = current_user.profile.study_program_id
        study_program = StudyProgram.query.get(study_program_id)
        modules=Module.query.filter_by(study_program_id=study_program_id).all()
        

        # Assume current_user.completed_modules is a list of completed module IDs
        completed_module_ids = {m.id for m in current_user.profile.completed_modules}

        # Only allow modules where all requirements are completed
        available_modules = []
        for module in modules:
            required_ids = [req.required_module_id for req in module.requirements]
            if all(rid in completed_module_ids for rid in required_ids):
                available_modules.append(module)

        form.module_id.choices = [(m.id, m.name) for m in available_modules]
        if form.validate_on_submit():
            selected_module_id = form.module_id.data
            selected_module= Module.query.get(selected_module_id)
            if selected_module not in current_user.profile.modules:
                current_user.profile.modules.append(selected_module_id)
                ScheduleService.add_module_sessions_to_schedule(current_user.profile, selected_module)
                flash('Module and its sessions added to your calendar!', 'success')
                db.session.commit()
            else:
                flash('You are already enrolled in this module.', 'warning')
            return redirect(url_for('student.my_modules'))

        return render_template('module/choose_module.html', form=form, study_program_name=study_program.name)
    
    except Exception as e:
        print(f"{e}")
        return render_template('module/choose_module.html', form=form, study_program_name=study_program.name)



# #FIXME: not sure if this belong here
# def assign_student_to_group(student_id, study_program_id):
#     """Simple group assignment logic"""
#     try:
#         # Find available group for this study program
#         available_group = Groups.query.filter_by(
#             study_program_id=study_program_id
#         ).first()
        
#         if available_group:
#             current_user.profile.group_id = available_group.id
        
#     except Exception as e:
#         print(f"Group assignment failed: {str(e)}")
