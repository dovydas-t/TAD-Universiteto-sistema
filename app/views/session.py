
from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from app.extensions import db
from app.forms.session_form import SessionForm
from app.models.session import Session
from app.models.module import Module
from app.utils.decorators import  admin_or_teacher_role_required



bp = Blueprint('session', __name__)


@bp.route('/add_session', methods=['GET', 'POST'])
@admin_or_teacher_role_required
def add_session():
    try:
        form = SessionForm()
        if current_user.profile.role.value == 'Teacher':
            teacher_modules = Module.query.filter(Module.teachers.any(id=current_user.profile.id)).all()
            modules = teacher_modules
        else:
            modules = Module.query.all()
        form.module_id.choices = [(m.id, m.name) for m in modules]

        if form.validate_on_submit():
            session = Session(
                module_id=form.module_id.data,
                type=form.type.data,
                date=form.date.data
            )
            db.session.add(session)
            db.session.commit()
            flash('Session added!', 'success')
            return redirect(url_for('session.add_session'))
        return render_template('session/add_session.html', form=form)
    except Exception as e:
        print(f"{e}")
        db.session.rollback()

@bp.route('/edit_session/<int:session_id>', methods=['GET', 'POST'])
@admin_or_teacher_role_required
def edit_session(session_id):
    my_session = Session.query.get_or_404(session_id)
    # Only allow if admin or the teacher of the module
    form = SessionForm(obj=my_session)
    if current_user.profile.role.value == 'Teacher':
        teacher_modules = Module.query.filter(Module.teachers.any(id=current_user.profile.id)).all()
        modules = teacher_modules
    else:
        modules = Module.query.all()
    form.module_id.choices = [(m.id, m.name) for m in modules]
    if form.validate_on_submit():
        my_session.module_id = form.module_id.data
        my_session.type = form.type.data
        my_session.date = form.date.data
        db.session.commit()
        flash('Sesija atnaujinta!', 'success')
        return redirect(url_for('session.session_list'))
    return render_template('session/edit_session.html', form=form, session=my_session)

@bp.route('/session/list')
@login_required
def session_list():
    # For teachers: show only their sessions
    if current_user.profile.role.value == 'Teacher':
        sessions = Session.query.join(Module).filter(Module.teachers.any(id=current_user.id)).all()
    # For admin: show all sessions
    elif current_user.profile.role.value == 'Admin':
        sessions = Session.query.all()
    else:
        flash('Access denied.', 'danger')
        return redirect(url_for('main.index'))
    return render_template('session/session_list.html', sessions=sessions)