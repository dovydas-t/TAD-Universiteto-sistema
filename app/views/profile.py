from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from app.forms.profile import ProfileForm
from app.extensions import db

from app.utils.decorators import admin_required
from app.utils.generate_avatar_url import  generate_avatar_url
from app.utils.save_profile_picture import save_profile_picture

bp = Blueprint('profile', __name__)

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
        user_changed = (
            form.username.data != current_user.username or
            form.first_name.data != current_user.profile.first_name or
            form.last_name.data != current_user.profile.last_name or
            form.email.data != current_user.profile.email or
            form.birth_date.data != current_user.profile.birth_date or
            form.study_program_id.data != current_user.profile.study_program_id or
            bool(form.profile_picture.data) # Just check if a file was uploaded
        )

        if not user_changed:
            flash("No changes detected.", "info")
            return redirect(url_for('main.profile'))

        # Check if username or email changed (affects avatar)
        username_changed = form.username.data != current_user.username
        email_changed = form.email.data != current_user.profile.email

        # Update fields
        current_user.username = form.username.data
        current_user.profile.first_name = form.first_name.data
        current_user.profile.last_name = form.last_name.data
        current_user.profile.email = form.email.data
        current_user.profile.birth_date = form.birth_date.data
        current_user.profile.study_program_id = form.study_program_id.data

        # Handle profile picture
        if form.profile_picture.data:
            # New picture uploaded
            filename = save_profile_picture(form.profile_picture.data, current_user.username)
            current_user.profile.profile_pic_path = filename
        elif username_changed or email_changed:
            # Only regenerate avatar if username/email changed and no new picture uploaded
            current_user.profile.profile_pic_path = generate_avatar_url(
                current_user.username, 
                current_user.profile.email
            )
        # If neither condition is met, keep the existing profile_pic_path

        db.session.commit()
        flash("Profile updated successfully!", "success")
        return redirect(url_for('main.profile'))
    
    return render_template("profile/update_profile.html", form=form)