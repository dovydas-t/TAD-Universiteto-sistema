from flask import Blueprint, flash, request, redirect, render_template, url_for
from flask_login import login_required, current_user
from app.models.module import Module
from app.forms.module import ModuleForm
from app.services.module_service import ModuleService
from app.services.study_program_service import StudyProgramService
from app.utils.decorators import admin_required

bp = Blueprint('module', __name__)

@bp.route('/')
def index():    
    return render_template('module/index.html',
                           title='TAD University Modules')

@bp.route('/detail/<int:module_id>')
def detail(module_id):
    """Display module details"""
    module = ModuleService.get_module_by_id(module_id)
    
    if not module:
        flash('Module not found.', 'error')
        return redirect(url_for('module.index'))
    
    return render_template('module/module_detail.html',
                           title='Module Detail',
                           module=module)

@bp.route('add_module', methods=['GET', 'POST'])
@admin_required
def add_module():
    """Add a new module"""
    form = ModuleForm()

    # Set choices first
    study_programs = StudyProgramService.get_all_study_programs()
    if not study_programs:
        flash('No study programs available. Please add a study program first.', 'warning')
        return redirect(url_for('study_program.add_study_program'))
    
    form.set_study_program_choices(study_programs)

    if request.method == 'GET':
        study_program_id = request.args.get('study_program_id')
        if study_program_id:
            form.study_program_id.data = int(study_program_id)
        return render_template('module/add_module.html', form=form, title='Add Module')

    if form.validate_on_submit():
        new_module = ModuleService.create_module_from_form(form)
        flash('Module added successfully!', 'success')
        return redirect(url_for('module.detail', module_id=new_module.id))
    
    

 