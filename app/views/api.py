from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models.auth import AuthUser
from app.services.faculty_service import FacultyService
from app.utils.decorators import json_required

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
