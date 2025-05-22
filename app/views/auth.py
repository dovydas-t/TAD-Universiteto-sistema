from datetime import datetime
from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from app.forms.auth import LoginForm, RegistrationForm, PasswordResetRequestForm, PasswordResetForm
from app.models import AuthUser, UserProfile
from app.extensions import db

bp = Blueprint('auth', __name__)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = AuthUser.query.filter_by(username=form.username.data).first()
        
        if user and user.check_password(form.password.data):
            if not user.is_active:
                flash('Account is deactivated. Contact support.', 'error')
                return redirect(url_for('auth.login'))
            
            # Update last login
            user.profile.last_login = db.func.current_timestamp()
            db.session.commit()

            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(next_page or url_for('main.dashboard'))
        
        flash('Invalid username or password', 'error')
    
    return render_template('auth/login.html', title='Sign In', form=form)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        #Get data from from
        username=form.username.data
        password=form.password.data
        password2=form.password2.data

        # Create user and user.profile and save user
        user = AuthUser(username=username)
        user.profile = UserProfile()
        # Function to hash given password
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', title='Register', form=form)


@bp.route('/reset-password-request', methods=['GET', 'POST'])
def reset_password_request():
    """Request password reset"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = PasswordResetRequestForm()
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


@bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Reset password with token"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    user = AuthUser.query.filter_by(reset_token=token).first()
    if not user or not user.verify_reset_token(token):
        flash('Invalid or expired reset token.', 'error')
        return redirect(url_for('auth.login'))
    
    form = PasswordResetForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        user.clear_reset_token()
        flash('Your password has been reset successfully.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/reset_password.html', title='Reset Password', form=form)


@bp.route('/verify-email/<token>')
def verify_email(token):
    """Verify email address"""
    user = AuthUser.query.filter_by(email_verification_token=token).first()
    if user and user.verify_email_token(token):
        flash('Email verified successfully!', 'success')
    else:
        flash('Invalid verification token.', 'error')
    return redirect(url_for('auth.login'))


@bp.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))

@bp.route('/delete_user', methods=['GET', 'POST'])
@login_required
def delete_user():
    """Delete the current user account"""

    # # Optional: delete related profile manually if not using cascading
    # profile = UserProfile.query.filter_by(user_id=user.id).first()
    # if profile:
    #     db.session.delete(profile)

    db.session.delete(current_user)
    db.session.commit()

    logout_user()
    flash('Your account has been deleted.', 'info')
    return redirect(url_for('main.index'))

