from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from app.forms.profile import ProfileForm
from app.extensions import db

from app.utils.decorators import admin_or_teacher_role_required

bp = Blueprint('users', __name__)

@bp.route('/list', methods=['GET', 'POST'])
@admin_or_teacher_role_required
def users_list():
    """User list page"""    
    return render_template('admin/users_list.html', title='Users List')