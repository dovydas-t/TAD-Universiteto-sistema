from flask import Blueprint, flash, request, redirect, render_template, url_for
from flask_login import login_required, current_user
from app.utils.decorators import admin_required
from app.forms.groups import GroupForm, EditGroupForm
from app.models.enum import RoleEnum
from app.models.profile import UserProfile
from app.services.study_program_service import StudyProgramService
from app.services.group_service import GroupsService
from app.services.user_service import UserService
from app.utils.decorators import admin_or_teacher_role_required

bp = Blueprint('groups', __name__)

@bp.route('/')
@admin_or_teacher_role_required
def index():
    groups = GroupsService.get_all_groups()
    return render_template('groups/groups_list.html', groups=groups)

@bp.route('/create_group', methods=['GET', 'POST'])
@admin_required
def create_group():
    form = GroupForm()
    
    # Populate the dropdown with study programs from DB
    study_programs = StudyProgramService.get_all_study_programs()
    if not study_programs:
        flash('No study programs available. Please add a study program first.', 'warning')
        return redirect(url_for('program.add_program'))
    
    form.study_program_id.choices = [(sp.id, sp.name) for sp in study_programs]
    
    if form.validate_on_submit():
        # Fetch the selected study program
        study_program = StudyProgramService.get_study_program_by_id(form.study_program_id.data)
        # Fetch existing group codes for the study program
        existing_group_codes = GroupsService.get_group_codes_by_study_program_id(study_program.id)

       

        group_code = StudyProgramService.generate_group_code_for_study_program(study_program, form.starting_year.data, existing_group_codes)

        # Create new group
        new_group = GroupsService.create_group_from_form(form, group_code)
        if not new_group:
            flash('Failed to create group. Please try again.', 'error')
            return redirect(url_for('groups.create_group'))
        
        flash(f'Group created. Group code: {group_code}', 'success')
        return redirect(url_for('groups.detail', group_id=new_group.id))
    
    # If GET request, prepopulate the form with study program ID if provided
    if request.method == 'GET':
        study_program_id = request.args.get('study_program_id')
        if study_program_id:
            form.study_program_id.data = int(study_program_id)
        
    return render_template('groups/create_group.html', form=form , title='Create Group')

@bp.route('/detail/<int:group_id>')
@admin_or_teacher_role_required
def detail(group_id):
    """Display group details"""
    group = GroupsService.get_group_by_id(group_id)
    students = UserService.get_students_by_group(group_id)

    if not group:
        flash('Group not found.', 'error')
        return redirect(url_for('index'))
    
    return render_template('groups/group_detail.html',
                           title='Group Detail',
                           group=group,
                           students=students)


@bp.route('/edit_group/<int:group_id>', methods=['GET', 'POST'])
def edit_group(group_id):
    group = GroupsService.get_group_by_id(group_id)
    students = UserService.get_students()
    assigned_students = UserService.get_students_by_group(group_id)
    teachers = UserService.get_all_teachers()

    form = EditGroupForm()

    # Set dynamic choices
    form.teacher_id.choices = [(t.id, t.full_name) for t in teachers]
    form.students.choices = [(s.id, s.full_name) for s in students]

    if form.validate_on_submit():
        UserService.update_user_group_from_form(form, group_id)
        flash("Group updated successfully!", "success")
        return redirect(url_for('groups.detail', group_id=group.id))

    # Pre-fill form with current selections
    form.students.data = [s.id for s in assigned_students]
    current_teacher = UserService.get_teacher_by_group(group_id)
    if current_teacher:
        form.teacher_id.data = current_teacher.id

    return render_template(
        'groups/edit_group.html',
        group=group,
        group_id=group_id,
        form=form,
        
    )

@bp.route('/delete_group/<int:group_id>', methods=['GET', 'POST'])
def delete_group(group_id):
    """Delete a group"""
    group = GroupsService.get_group_by_id(group_id)
    students = UserService.get_students_by_group(group_id)

    if not group:
        flash('Group not found.', 'error')
        return redirect(url_for('groups.index'))
    
    GroupsService.delete_group(group_id)
    flash('Group deleted successfully.', 'success')

    if students:
    # If there are students in the group, reassign them to new groups
        flash(f"Group has {len(students)} students assigned. Reassigning students...", 'warning')

        # Reassign students to new groups
        for student in students:
            new_group_id = GroupsService.auto_assign_to_group(student.study_program_id)
            UserService.update_user_group(student.id, new_group_id)
            print(f"Debug: Student {student.full_name} assigned to new group {new_group_id}")
        flash('Students have been reassigned to new groups.', 'success')

    return redirect(url_for('groups.index'))
    
    



    
    

@bp.route('/group-info')
@login_required
def group_info():
    """View group information"""
    if not current_user.profile.group_id:
        flash('You are not assigned to any group.', 'info')
        return redirect(url_for('main.student_dashboard'))
    
    group = current_user.profile.group_id
    
    # Get all students in this group
    group_members = UserProfile.query.filter_by(
        group_id=group.id,
        role=RoleEnum.Student
    ).all()
    
    return render_template('groups/groups_info.html',
                         group=group,
                         group_members=group_members)
