from flask import Blueprint, jsonify, request, session
from flask_login import login_required, current_user
from sqlalchemy import or_
from app.utils.decorators import json_required
from app.models.auth import AuthUser
from app.services.faculty_service import FacultyService
from app.services.group_service import GroupsService
from app.utils.decorators import admin_or_teacher_role_required
from app.models.profile import UserProfile
from app.models.enum import RoleEnum
from app.services.test_question_service import TestQuestionService
from app.services.test_service import TestService
from app.services.grade_service import GradeService


bp = Blueprint('api', __name__)


@bp.route('/users/<int:user_id>')
@login_required
def get_user(user_id):
    """Get user information"""
    user = AuthUser.query.get_or_404(user_id)
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'full_name': user.full_name,
        'created_at': user.created_at.isoformat()
    })


@bp.route('/profile', methods=['PUT'])
@login_required
@json_required
def update_profile():
    """Update user profile via API"""
    data = request.get_json()
    
    if 'first_name' in data:
        current_user.first_name = data['first_name']
    if 'last_name' in data:
        current_user.last_name = data['last_name']
    
    from app.extensions import db
    db.session.commit()
    
    return jsonify({
        'message': 'Profile updated successfully',
        'user': {
            'id': current_user.id,
            'full_name': current_user.full_name
        }
    })

@bp.route('/faculty_detail/<int:faculty_id>')
def faculty_detail(faculty_id):
    faculty = FacultyService.get_faculty_by_id(faculty_id)
    if faculty is None:
        return jsonify({'error': 'Faculty not found'}), 404

    return jsonify({
        'id': faculty.id,
        'name': faculty.name,
        'description': faculty.description,
        'full_address': faculty.get_full_address(),
        'programs': [program.name for program in faculty.programs]  # optional
    })

@bp.route('/groups/<int:study_program_id>', methods=['GET'])
def get_groups_by_study_program(study_program_id):
    groups = GroupsService.get_all_groups()

    print("Requested study_program_id:", study_program_id)
    for g in groups:
        print("Group:", g.id, g.code, "Program ID:", g.study_program_id)
        
    filtered = [(g.id, g.code) for g in groups if g.study_program_id == study_program_id]
    return jsonify(filtered)

@bp.route('users/list', methods=['GET'])
@admin_or_teacher_role_required
def user_list():
    # Get and sanitize query parameters
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    search = request.args.get('search', '', type=str).strip()
    role = request.args.get('role', type=str)
    group_id = request.args.get('group_id', type=int)
    study_program_id = request.args.get('study_program_id', type=int)

    # Limit per_page to accepted values only
    if per_page not in [10, 25, 50, 100]:
        per_page = 10

    # Base query
    query = UserProfile.query

    # Search filter (name or email)
    if search:
        search_pattern = f"%{search}%"
        query = query.filter(
            or_(
                UserProfile.first_name.ilike(search_pattern),
                UserProfile.last_name.ilike(search_pattern),
                UserProfile.email.ilike(search_pattern)
            )
        )

    # Role filter
    if role:
        try:
            role_enum = RoleEnum[role.capitalize()]
            query = query.filter_by(role=role_enum)
        except KeyError:
            return jsonify({"error": "Invalid role specified"}), 400

    # Group filter
    if group_id:
        query = query.filter_by(group_id=group_id)

    # Study program filter
    if study_program_id:
        query = query.filter_by(study_program_id=study_program_id)

    # Order and paginate
    pagination = query.order_by(UserProfile.last_name.asc(), UserProfile.first_name.asc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    users = pagination.items

    # Serialize
    result = []
    for user in users:
        result.append({
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "role": user.role.value,
            "group_id": user.group_id,
            "study_program_id": user.study_program_id,
            "is_active": user.is_active,
            "created_at": user.created_at.isoformat()
        })

    # Final response
    return jsonify({
        "total": pagination.total,
        "page": page,
        "per_page": per_page,
        "users": result
    })

@bp.route('/test/question/<int:question_id>', methods=['GET'])
def get_question(question_id):
    """Get question details by ID"""
    question = TestQuestionService.get_test_question_by_id(question_id)
    return jsonify({
        "id": question.id,
        "text": question.question_text,
        "answers": [
            {"id": ao.id, "text": ao.option_text}
            for ao in question.answer_options
        ]
    })

@bp.route('/test/submit', methods=['POST'])
def submit_answer():
    """Submit an answer to a test question"""
    print('Headers:', request.headers)
    print('Content-Type:', request.content_type)
    print('Raw Data:', request.data)
    data = request.json
    print(f"Received data: {data}")
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    question_id = data.get('question_id')
    selected_answers = data.get('selected_answers', [])

    if question_id is None or not isinstance(selected_answers, list):
        return jsonify({"error": "Invalid input data"}), 400

    # Optional: Validate or store selected answers here
    submitted = session.get('submitted_answers', {})
    submitted[str(question_id)] = selected_answers
    session['submitted_answers'] = submitted
    print(f"User answered question {question_id} with answers {selected_answers}")
    return jsonify({"success": True})

@bp.route("/test/finish/<int:test_id>", methods=["POST"])
@login_required
def finish_test(test_id):
    try:
        submitted = session.pop("submitted_answers", {})  # Clear after use

        correct_count = 0
        for question_id, selected_answers in submitted.items():
            if TestQuestionService.check_submitted_answer(int(question_id), selected_answers):
                correct_count += 1

        grade = TestService.calculate_grade(correct_count, total_questions=len(submitted))
        GradeService.add_grade_for_student(current_user.id, test_id, grade)

        return jsonify({"grade": grade})
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": "An error occurred while finishing the test"}), 500