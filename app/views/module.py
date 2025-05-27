from flask import Blueprint, request, redirect, render_template
from flask_login import login_required, current_user
from app.services.module_service import ModuleService
from app.models.module import Module


bp = Blueprint('module', __name__)

@bp.route('/')
def index():    
    return render_template('module/index.html',
                           title='TAD University Modules')
