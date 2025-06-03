from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from app.extensions import db
from app.forms.profile import ProfileForm
from app.forms.session_form import SessionForm
from app.models.enum import RoleEnum
from app.models.module import Module
from app.models.session import Session


from app.utils.decorators import admin_required, teacher_status_required, admin_or_teacher_role_required

bp = Blueprint('main', __name__)


@bp.route('/')
@bp.route('/index')
def index():
    """Home page"""
    return render_template('index.html', title='Home')

@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """User profile page"""    
    return render_template('profile.html', title='Profile')

@bp.route('/profile/update', methods=['GET', 'POST'])
@login_required
def profile_update():
    """User profile update"""
    form = ProfileForm(obj=current_user.profile)    
    if form.validate_on_submit():
        #TODO: Cia galbut reiketu sukurti papildomas funkcijas, kad kodas butu svaresnis
        # galbut galima butu panaudoti '__eq__' magic dunder
        user_changed = (
            form.username.data != current_user.username or
            form.first_name.data != current_user.profile.first_name or
            form.last_name.data != current_user.profile.last_name or
            form.email.data != current_user.profile.email or
            form.birth_date.data != current_user.profile.birth_date
        )

        if not user_changed:
            flash("No changes detected.", "info")
            return redirect(url_for('main.profile'))

        # Proceed with updating only if something changed
        current_user.username = form.username.data
        current_user.profile.first_name = form.first_name.data
        current_user.profile.last_name = form.last_name.data
        current_user.profile.email = form.email.data
        current_user.profile.birth_date = form.birth_date.data

        db.session.commit()
        flash("Profile updated successfully!", "success")
        return redirect(url_for('main.profile'))

    return render_template("profile/update_profile.html", form=form)




@bp.route('/privacy')
def privacy():
    return render_template('admin/privacy.html')

@bp.route('/accessibility')
def accessibility():
    return render_template('admin/accessibility.html')

@bp.route('/media')
def media():
    return render_template('admin/media.html')