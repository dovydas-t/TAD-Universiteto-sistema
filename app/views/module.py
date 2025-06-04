from flask import Blueprint, flash, request, redirect, render_template, url_for
from flask_login import login_required, current_user
from app.extensions import db
from app.models.module import Module
from app.models.study_program import StudyProgram
from app.forms.module import ModuleForm, AddModuleRequirementForm
from app.forms.choosemodule import ChooseModule
from app.forms.module import ModuleForm
from app.services.module_service import ModuleService
from app.services.study_program_service import StudyProgramService
from app.utils.decorators import admin_required, admin_or_teacher_role_required
from app.services.schedule_service import ScheduleService 


bp = Blueprint('module', __name__)

@bp.route('/')
def index():    
    return render_template('module/index.html',
                           title='TAD University Modules')

@bp.route('/detail/<int:module_id>')
def detail(module_id):
    """Display module details"""
    try:
        module = ModuleService.get_module_by_id(module_id)
        
        if not module:
            flash('Module not found.', 'error')
            return redirect(url_for('module.index'))
        
        return render_template('module/module_detail.html',
                            title='Module Detail',
                            module=module)
    except Exception as e:
        print(f"{e}")
        return render_template('module/module_detail.html',
                            title='Module Detail',
                            module=module)

@bp.route('add_module', methods=['GET', 'POST'])
@admin_or_teacher_role_required
def add_module():
    """Add a new module"""
    try:
        form = ModuleForm()
        # Set choices first

        if current_user.profile.role.value == 'Teacher':
            if not current_user.profile.study_program:
                flash('You are not assigned to any study program. Please contact admin.', 'danger')
                return redirect(url_for('module.index'))
            study_programs = [current_user.profile.study_program]
        else:
            study_programs = StudyProgramService.get_all_study_programs()
        
        study_programs = [sp for sp in study_programs if sp is not None]    
        form.set_study_program_choices(study_programs)

        if request.method == 'GET':
            study_program_id = request.args.get('study_program_id')
            
            if study_program_id:
                form.study_program_id.data = int(study_program_id)
            return render_template('module/add_module.html', form=form, title='Add Module')

        if form.validate_on_submit():
            new_module = ModuleService.create_module_from_form(form)
        if current_user.profile.role.value == 'Teacher':
            new_module.teachers.append(current_user.profile)
            new_module.created_by = current_user.profile  # <-- set creator
            db.session.commit()
        flash('Module added successfully!', 'success')
        return redirect(url_for('module.detail', module_id=new_module.id))
    except Exception as e:
        print(f"{e}")
        db.session.rollback()
        return render_template('module/add_module.html', form=form, title='Add Module')
    

@bp.route('module_list', methods=['GET', 'POST'])
@login_required
def module_list():

    try: 

        if current_user.profile.role.value == 'Teacher':
            # Only modules created by this teacher
            module_list = Module.query.filter_by(created_by_id=current_user.profile.id).all()
        else:
            module_list = ModuleService.get_all_modules() or []
        module_names = [module.name for module in module_list]

        if not module_list:
            return render_template('module/no_module.html',
                                title='No Modules Available')
        
        return render_template('module/modules_list.html',
                            title='TAD University Modules',
                            module_list=module_list,
                            module_names=module_names)
    except Exception as e:
        print(f"{e}")
    return render_template('module/modules_list.html',
                           title='TAD University Modules',
                           module_list=module_list,
                           module_names=module_names)
    
@bp.route('add_requirement/<int:module_id>', methods=['GET', 'POST'])
@admin_or_teacher_role_required
def add_requirement(module_id):
    """Add a requirement to a module"""
    module = ModuleService.get_module_by_id(module_id)

    if not module:
        flash('Module not found.', 'error')
        return redirect(url_for('module.list'))  # Redirect somewhere appropriate

    form = AddModuleRequirementForm()

    other_modules = ModuleService.get_all_modules_except(module_id)
    form.set_module_choices(other_modules)

    if form.validate_on_submit():
        requirement_id = form.requirement_id.data
        success = ModuleService.add_prerequisite(module.id, requirement_id)

        if success:
            flash('Requirement added successfully!', 'success')
        else:
            flash('Failed to add requirement. It may already exist or be invalid.', 'error')
        
        return redirect(url_for('module.detail', module_id=module.id))

    return render_template('module/add_requirement.html', form=form, module=module)




 