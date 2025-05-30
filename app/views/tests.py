from flask import Blueprint, flash, request, redirect, render_template, url_for
from flask_login import login_required, current_user
from app.utils.decorators import admin_required
from app.services.test_service import TestService


bp = Blueprint('test', __name__)

@bp.route('/')
def index():    
    return render_template('module/index.html',
                           title='TAD University Modules')

@bp.route('/detail/<int:test_id>')
def detail(test_id):
    """Display test details"""
    test = TestService.get_test_by_id(test_id)
    
    if not test:
        flash('Test not found.', 'error')
        return redirect(url_for('test.index'))
    
    return render_template('tests/test_detail.html',
                           title='Test Detail',
                           test=test)