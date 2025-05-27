from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from app.forms.profile import ProfileForm
from app.extensions import db
from app.utils.decorators import admin_required

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
            #TODO: Cia galbut reiketu sukurti papildomas funkcijas, kad kodas butu svaresnis
            # galbut galima butu panaudoti '__eq__' magic dunder
            form.username.data != current_user.username or
            form.first_name.data != current_user.profile.first_name or
            form.last_name.data != current_user.profile.last_name or
            form.email.data != current_user.profile.email or
            form.birth_date.data != current_user.profile.birth_date or
            form.study_program_id.data != current_user.profile.study_program_id
        )

        if not user_changed:
            flash("No changes detected.", "info")
            return redirect(url_for('profile'))

        # Proceed with updating only if something changed
        current_user.username = form.username.data
        current_user.profile.first_name = form.first_name.data
        current_user.profile.last_name = form.last_name.data
        current_user.profile.email = form.email.data
        current_user.profile.birth_date = form.birth_date.data
        current_user.profile.study_program_id = form.study_program_id.data 

        db.session.commit()
        flash("Profile updated successfully!", "success")
        return redirect(url_for('profile'))
    return render_template("profile/update_profile.html", form=form)