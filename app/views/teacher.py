from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from app.extensions import db
from app.utils.decorators import teacher_status_required

bp = Blueprint('teacher', __name__)



