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
        study_programs = StudyProgramService.get_all_study_programs()
        if not study_programs:
            flash('No study programs available. Please add a study program first.', 'warning')
            return redirect(url_for('study_program.add_study_program'))
        
        form.set_study_program_choices(study_programs)
        all_modules = Module.query.all()
        form.set_prerequisite_choices(all_modules)

        if request.method == 'GET':
            study_program_id = request.args.get('study_program_id')
            if study_program_id:
                form.study_program_id.data = int(study_program_id)
            return render_template('module/add_module.html', form=form, title='Add Module')

        if form.validate_on_submit():
            new_module = ModuleService.create_module_from_form(form)
            for prereq_id in form.prerequisites.data:
                ModuleService.add_prerequisite(new_module.id, prereq_id)
            flash('Module added successfully!', 'success')
            return redirect(url_for('module.detail', module_id=new_module.id))
    except Exception as e:
        print(f"{e}")
    

@bp.route('module_list', methods=['GET', 'POST'])
@login_required
def module_list():

    try: 

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
            if selected_module_id not in current_user.profile.modules:
                current_user.profile.modules.append(selected_module_id)
                ScheduleService.add_module_sessions_to_schedule(current_user.profile, selected_module_id)
                flash('Module and its sessions added to your calendar!', 'success')
                db.session.commit()
            else:
                flash('You are already enrolled in this module.', 'warning')
            return redirect(url_for('student.my_modules'))

        return render_template('module/choose_module.html', form=form, study_program_name=study_program.name)
    
    except Exception as e:
        print(f"{e}")
        return render_template('module/choose_module.html', form=form, study_program_name=study_program.name)


 