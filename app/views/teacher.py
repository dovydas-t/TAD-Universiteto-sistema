from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from app.extensions import db
from app.utils.decorators import teacher_status_required

bp = Blueprint('teacher', __name__)

@bp.route('/', methods=['GET'])
@login_required
@teacher_status_required
def dashboard():
    """Teacher dashboard"""    
    return render_template('teacher/dashboard.html', title='Teacher Dashboard')

