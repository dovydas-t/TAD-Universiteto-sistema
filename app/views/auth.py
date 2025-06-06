from datetime import datetime
from MySQLdb import IntegrityError
from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required, user_logged_in
from app.forms.auth import LoginForm, RegistrationForm, PasswordForm, EnterEmailForm
from app.forms.profile_setup_form import ProfileSetupForm
from app.models.auth import AuthUser
from app.models.enum import RoleEnum
from app.models.profile import UserProfile
from app.extensions import db
from app.utils.generate_avatar_url import generate_avatar_url
from app.utils.save_profile_picture import save_profile_picture
from app.services.group_service import GroupsService
from app.services.user_service import UserService
from app.utils.decorators import admin_or_teacher_role_required

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login with blocking mechanism"""
    try:
        if current_user.is_authenticated:
            return redirect(url_for('dashboard.dashboard'))
        
        form = LoginForm()
        if form.validate_on_submit():
            user = AuthUser.query.filter_by(username=form.username.data).first()
            
            if user:
                # NEW: Check if user is blocked
                if user.is_blocked():
                    remaining_time = user.get_time_until_unblock()
                    flash(f'Account temporarily blocked due to failed login attempts. Try again in {remaining_time} minutes.', 'error')
                    return render_template('auth/login.html', title='Sign In', form=form)
                
                # Check password
                if user.check_password(form.password.data):
                    # Check if account is active
                    if not user.is_active:
                        flash('Account is deactivated. Contact support.', 'error')
                        return redirect(url_for('auth.login'))
                    
                    # NEW: Record successful login and reset failed attempts
                    user.record_successful_login()
                    
                    login_user(user, remember=form.remember_me.data)

                    # Update last login in profile (keep your existing logic)
                    user.profile.last_login = db.func.current_timestamp()
                    db.session.commit()

                    next_page = request.args.get('next')
                    flash(f'Login successful! Welcome back, {user.username}!', 'success')
                    return redirect(next_page or url_for('main.index'))
                else:
                    # NEW: Wrong password - record failed attempt
                    user.record_failed_login()
                    if user.failed_login_attempts >= 3:
                        flash('Too many failed attempts. Account temporarily blocked for 15 minutes.', 'error')
                    else:
                        remaining_attempts = 3 - user.failed_login_attempts
                        flash(f'Invalid password. {remaining_attempts} attempts remaining.', 'error')
            else:
                # User doesn't exist
                flash('Invalid username or password', 'error')
        
        return render_template('auth/login.html', title='Sign In', form=form)
    except Exception as e:
        print(f"{e}")
        return render_template('auth/login.html', title='Sign In', form=form)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration - Step 1"""

    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
        
    form = RegistrationForm()
    if form.validate_on_submit():
        # Get data from form
        username = form.username.data
        study_program_id = form.study_program_id.data
        password = form.password.data
        password2 = form.password2.data
        
        role_value = form.role.data  # This will be 'Student' or 'Teacher'
        
        # Convert string to enum
        role = RoleEnum(role_value)  # Direct conversion since values match

        # Create user and user.profile and save user
        user = AuthUser(username=username)  
        user.profile = UserProfile(role=role)

        if study_program_id and study_program_id != 0:
            user.profile.study_program_id = study_program_id
            group_id = GroupsService.auto_assign_to_group(study_program_id)
            
            if group_id:
                user.profile.group_id = group_id
        
        # Generate default avatar URL using username only
        user.profile.profile_pic_path = generate_avatar_url(username)
        
        # Function to hash given password
        user.set_password(password)
        try:
            # Add user and profile to the session and commit
            db.session.add(user)
            db.session.add(user.profile)
            db.session.commit()
            
            # Auto-login the user for step 2
            login_user(user)
            
            flash('Account created! Please complete your profile.', 'info')
            return redirect(url_for('auth.profile_setup'))  # Redirect to step 2
        
        except IntegrityError as e:
            db.session.rollback()
            if "Duplicate entry" in str(e.orig):
                flash("This email is already in use. Please choose a different one.", "danger")
            else:
                flash("A database integrity error occurred.", "danger")
            return render_template('auth/profile_setup.html')

        except Exception as e:
            db.session.rollback()
            print(f"Unexpected error: {e}")
            flash("An unexpected error occurred.", "danger")
            return render_template('auth/profile_setup.html')
    
    return render_template('auth/register.html', title='Register', form=form)

@bp.route('/profile-setup', methods=['GET', 'POST'])
@login_required
def profile_setup():
    """User registration - Step 2: Profile Setup"""
    form = ProfileSetupForm()
    if form.validate_on_submit():
        try:
            # Update profile with all details including email
            current_user.profile.email = form.email.data
            current_user.profile.first_name = form.first_name.data
            current_user.profile.last_name = form.last_name.data
            current_user.profile.birth_date = form.birth_date.data
            
            # Update avatar URL to use email now
            current_user.profile.profile_pic_path = generate_avatar_url(
                current_user.username, 
                form.email.data
            )
            
            # Handle profile picture upload if provided
            if form.profile_picture.data:
                filename = save_profile_picture(form.profile_picture.data, current_user.username)
                current_user.profile.profile_pic_path = filename
                        
            db.session.commit()
            
            flash('Profile completed successfully!', 'success')
            return redirect(url_for('dashboard.dashboard'))
        except Exception as e:
            print(f"{e}")
            
    
    return render_template('auth/profile_setup.html', title='Complete Profile', form=form)

@bp.route('/reset-password-request', methods=['GET', 'POST'])
def reset_password_request():
    """Request password reset"""
    try:
        if current_user.is_authenticated:
            return redirect(url_for('main.index'))
        
        form = EnterEmailForm()
        if form.validate_on_submit():
            user = AuthUser.query.filter_by(email=form.email.data).first()
            if user:
                token = user.generate_reset_token()
                # In a real app, send reset email here
                flash('Check your email for password reset instructions.', 'info')
            else:
                flash('Email address not found.', 'error')
            return redirect(url_for('auth.login'))
        
        return render_template('auth/reset_password_request.html', title='Reset Password', form=form)
    except Exception as e:
        print(f"{e}")
        db.session.rollback()

@bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Reset password with token"""
    try: 
        if current_user.is_authenticated:
            return redirect(url_for('main.index'))
        
        user = AuthUser.query.filter_by(reset_token=token).first()
        if not user or not user.verify_reset_token(token):
            flash('Invalid or expired reset token.', 'error')
            return redirect(url_for('auth.login'))
        
        form = PasswordForm()
        if form.validate_on_submit():
            user.set_password(form.password.data)
            user.clear_reset_token()
            flash('Your password has been reset successfully.', 'success')
            return redirect(url_for('auth.login'))
        
        return render_template('auth/reset_password.html', title='Reset Password', form=form)
    except Exception as e:
        print(f"{e}")
        db.session.rollback()


# @bp.route('/verify-email/<token>')
# def verify_email(token):
#     """Verify email address"""
#     user = AuthUser.query.filter_by(email_verification_token=token).first()
#     if user and user.verify_email_token(token):
#         flash('Email verified successfully!', 'success')
#     else:
#         flash('Invalid verification token.', 'error')
#     return redirect(url_for('auth.login'))


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.index'))

    

@bp.route('/delete_user/<int:user_id>', methods=['GET', 'POST'])
@admin_or_teacher_role_required
def delete_user(user_id):
    """Delete user account"""
    user = UserService.get_user_profile(user_id)
    flash(f'User {user.full_name} has been deleted.', 'success')
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('users.users_list'))

@bp.route('/request-user-delete', methods=['GET', 'POST'])
@login_required
def request_user_delete():
    """Request user account deletion"""
    try:
        form = PasswordForm()
        if form.validate_on_submit():
            if current_user.check_password(form.password.data):
                db.session.delete(current_user)
                db.session.commit()
                logout_user()
                flash("Your account has been deleted.", 'success')
                return redirect(url_for('main.index'))
            else:
                flash("Incorrect password. Please try again.", 'danger')

        return render_template('auth/delete_user_request.html', title='Delete Account', form=form)
    except Exception as e:
        print(f"{e}")
        db.session.rollback()



#--------------------------------------------------------------------------------
# @bp.route('/reset-password/<token>', methods=['GET', 'POST'])
# def reset_password(token):
#     """Reset password with token"""
#     if current_user.is_authenticated:
#         return redirect(url_for('main.index'))
    
#     user = AuthUser.query.filter_by(reset_token=token).first()
#     if not user or not user.verify_reset_token(token):
#         flash('Invalid or expired reset token.', 'error')
#         return redirect(url_for('auth.login'))
    
#     form = PasswordForm()
#     if form.validate_on_submit():
#         user.set_password(form.password.data)
#         user.clear_reset_token()
#         flash('Your password has been reset successfully.', 'success')
#         return redirect(url_for('auth.login'))
    
#     return render_template('auth/reset_password.html', title='Reset Password', form=form)