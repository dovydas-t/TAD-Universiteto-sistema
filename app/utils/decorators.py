from functools import wraps
from flask import request, jsonify
from flask_login import current_user, login_required

from app.models.profile import RoleEnum


def json_required(f):
    """Decorator to ensure request contains JSON data"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.is_json:
            return jsonify({'error': 'Content-Type must be application/json'}), 400
        return f(*args, **kwargs)
    return decorated_function

# Not sure if it works with @login-required inside
def admin_required(f):
    """Decorator to require admin privileges"""
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if current_user.profile.role != RoleEnum.Admin:
            return jsonify({'error': 'Admin privileges required'}), 403
        return f(*args, **kwargs)
    return decorated_function

def teacher_status_required(f):
    """Decorator to require teacher privileges"""
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if current_user.profile.role != RoleEnum.Teacher:
            return jsonify({'error': 'Teacher privileges required'}), 403
        return f(*args, **kwargs)
    return decorated_function

            



#DONE: seni decodatoriai
# def admin_required(f):
#     """Decorator to require admin privileges"""
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if not current_user.is_authenticated or not getattr(current_user.profile, 'is_admin', False):
#             return jsonify({'error': 'Admin privileges required'}), 403
#         return f(*args, **kwargs)
#     return decorated_function

# def teacher_status_required(f):
#     """Decorator to require current_user.profile.is_teacher"""
#     def decorated_function(*args, **kwargs):
#         if not current_user.is_authenticated or not getattr(current_user.profile, 'is_teacher', False):
#             return jsonify({'error': 'Teacher privileges required'}), 403
#         return f(*args, **kwargs)
#     return decorated_function