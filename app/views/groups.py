from flask import Blueprint, flash, request, redirect, render_template, url_for
from flask_login import login_required, current_user
from app.utils.decorators import admin_required
from app.forms.groups import GroupForm
from app.models import Groups
from app.services.study_program_service import StudyProgramService
from app.services.group_service import GroupsService
from app.utils.decorators import admin_or_teacher_role_required

bp = Blueprint('groups', __name__)


@bp.route('/')
@admin_or_teacher_role_required
def index():
    return render_template('groups/groups.html')


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
    
    if not group:
        flash('Group not found.', 'error')
        return redirect(url_for('index'))
    
    return render_template('groups/group_detail.html',
                           title='Group Detail',
                           group=group)
