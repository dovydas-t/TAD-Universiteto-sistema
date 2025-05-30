from flask import render_template, redirect, url_for, flash, Blueprint
from flask_login import login_required, current_user
from app.extensions import db
from app.services.user_service import UserService
from app.services.module_service import ModuleService
from app.forms.student_form import StudentEditForm
from app.utils.decorators import admin_or_teacher_role_required
from collections import defaultdict
# Create blueprint for student routes
bp = Blueprint('student', __name__, url_prefix='/student')


@bp.route('')
def test():
    pass
    

@bp.route('/detail/<int:student_id>', methods=['GET', 'POST'])
@login_required
def detail(student_id):
    student, grades = UserService.get_student_and_student_grades(student_id)

    if not student:
        flash('Error: No student at ID: {{ student.id }})', 'error')
        return redirect(url_for('module.index'))
    
    module_grade_map = defaultdict(list)
    for grade in grades:
        module = ModuleService.get_module_by_id(grade.module_id)
        module_grade_map[module.name].append(grade.grade)
    
    return render_template('student/student_detail.html',
                           title='Student Details',
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









# @bp.route('/register', methods=['GET', 'POST'])
# @login_required
# def register():
#     """
#     Main hybrid registration route - handles both immediate and approval cases
#     """
#     form = HybridRegistrationForm()
    
#     if form.validate_on_submit():
#         try:
#             study_program_id = form.study_program_id.data
#             module_id = form.module_id.data
#             student_notes = form.student_notes.data
#             student_id = current_user.profile.id
            
#             # Use decision engine to determine path
#             decision_engine = RegistrationDecisionEngine()
#             decision, reasons = decision_engine.evaluate_registration(
#                 student_id, study_program_id, module_id
#             )
            
#             if decision == 'immediate':
#                 # IMMEDIATE REGISTRATION PATH
#                 success = process_immediate_registration(
#                     student_id, study_program_id, module_id
#                 )
                
#                 if success:
#                     flash('🎉 Registration successful! You are now enrolled.', 'success')
#                     return redirect(url_for('student.registration_success'))
#                 else:
#                     flash('Registration failed. Please try again.', 'error')
            
#             else:
#                 # APPROVAL REQUIRED PATH
#                 success = create_approval_request(
#                     student_id, study_program_id, module_id, reasons, student_notes
#                 )
                
#                 if success:
#                     flash('Your registration requires admin approval:', 'warning')
#                     for reason in reasons:
#                         flash(f'• {reason}', 'warning')
#                     flash('Your request has been submitted for review.', 'info')
#                     return redirect(url_for('student.my_requests'))
#                 else:
#                     flash('Failed to submit approval request.', 'error')
                    
#         except Exception as e:
#             db.session.rollback()
#             flash(f'Registration error: {str(e)}', 'error')
    
#     return render_template('student/register.html', form=form)


# @bp.route('/registration-success')
# @login_required
# def registration_success():
#     """
#     Show registration success with schedule and group info
#     """
#     student_id = current_user.profile.id
    
#     # Get latest enrolled module (most recent grade entry with NULL)
#     latest_enrollment = Grade.query.filter(
#         Grade.student_id == student_id,
#         Grade.grade.is_(None)
#     ).order_by(Grade.id.desc()).first()
    
#     if not latest_enrollment:
#         flash('No recent registration found.', 'warning')
#         return redirect(url_for('student.dashboard'))
    
#     module = Module.query.get(latest_enrollment.module_id)
#     study_program = current_user.profile.study_program
#     group = current_user.profile.group
    
#     # Get schedule for this module
#     schedule_items = ScheduleItem.query.filter_by(module_id=module.id).all()
    
#     return render_template('student/registration_success.html',
#                          module=module,
#                          study_program=study_program,
#                          group=group,
#                          schedule_items=schedule_items)


# @bp.route('/my-requests')
# @login_required
# def my_requests():
#     """
#     Show student's registration requests and their status
#     """
#     student_id = current_user.profile.id
    
#     # Get all requests for this student
#     requests = RegistrationRequest.query.filter_by(
#         student_id=student_id
#     ).order_by(RegistrationRequest.created_at.desc()).all()
    
#     # Separate by status
#     pending_requests = [req for req in requests if req.status == 'pending']
#     processed_requests = [req for req in requests if req.status != 'pending']
    
#     return render_template('student/my_requests.html',
#                          pending_requests=pending_requests,
#                          processed_requests=processed_requests)


# @bp.route('/dashboard')
# @login_required
# def dashboard():
#     """
#     Student dashboard showing current registrations and options
#     """
#     student_id = current_user.profile.id
    
#     # Get enrolled modules
#     enrolled_grades = Grade.query.filter(
#         Grade.student_id == student_id,
#         Grade.grade.is_(None)
#     ).all()
#     enrolled_modules = [Module.query.get(grade.module_id) for grade in enrolled_grades]
    
#     # Get completed modules
#     completed_grades = Grade.query.filter(
#         Grade.student_id == student_id,
#         Grade.grade.isnot(None),
#         Grade.grade >= 50.0
#     ).all()
#     completed_modules = [Module.query.get(grade.module_id) for grade in completed_grades]
    
#     # Get pending requests count
#     pending_count = RegistrationRequest.query.filter_by(
#         student_id=student_id,
#         status='pending'
#     ).count()
    
#     return render_template('student/dashboard.html',
#                          enrolled_modules=enrolled_modules,
#                          completed_modules=completed_modules,
#                          pending_count=pending_count,
#                          study_program=current_user.profile.study_program,
#                          group=current_user.profile.group)


# def process_immediate_registration(student_id, study_program_id, module_id):
#     """Process immediate registration"""
#     try:
#         # Update study program
#         current_user.profile.study_program_id = study_program_id
#         current_user.profile.updated_at = datetime.utcnow()
        
#         # Create grade entry
#         grade_entry = Grade(
#             student_id=student_id,
#             module_id=module_id,
#             grade=None
#         )
#         db.session.add(grade_entry)
        
#         # Assign to group (simple logic)
#         assign_student_to_group(student_id, study_program_id)
        
#         db.session.commit()
#         return True
        
#     except Exception as e:
#         db.session.rollback()
#         print(f"Immediate registration failed: {str(e)}")
#         return False


# def create_approval_request(student_id, study_program_id, module_id, reasons, student_notes):
#     """Create approval request"""
#     try:
#         request = RegistrationRequest(
#             student_id=student_id,
#             study_program_id=study_program_id,
#             module_id=module_id,
#             reason=', '.join(reasons),
#             student_notes=student_notes,
#             status='pending'
#         )
#         db.session.add(request)
#         db.session.commit()
#         return True
        
#     except Exception as e:
#         db.session.rollback()
#         print(f"Failed to create approval request: {str(e)}")
#         return False



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
