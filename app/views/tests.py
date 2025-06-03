from flask import Blueprint, flash, request, redirect, render_template, url_for
from flask_login import login_required, current_user
from app.extensions import db
from app.models.module import Module
from app.models.test import Test
from app.forms.test_form import TestForm
from app.utils.decorators import admin_required
from app.services.test_service import TestService


bp = Blueprint('test', __name__)

@bp.route('/')
@login_required
def index():
    """Display all tests"""
    tests = TestService.get_all_tests()
    return render_template('tests/tests.html',
                           title='Test',
                           tests=tests)

@bp.route('/test/create',  methods=['GET','POST'])
def create_test():
    form = TestForm()
    modules = Module.query.all()
    form.module_id.choices = [(m.id,m.name) for m in modules]
    
    if form.validate_on_submit():
        name=form.name.data
        module_id=form.module_id.data
        test = Test(name=name, module_id=module_id )
        db.session.add(test)
        db.session.commit()
        flash('Test created! Now add questions.', 'success')
        return redirect(url_for('test_question.add_question', test_id=test.id))
    return render_template('tests/create_test.html', form=form)

@bp.route('/test/<int:test_id>', methods=['GET', 'POST'])
@login_required
def take_test(test_id):
    """Take a test"""
    test = TestService.get_test_by_id(test_id)    
    if not test:
        flash('Test not found.', 'error')
        return redirect(url_for('test.index'))
    serialized_questions = []
    for question in test.questions:
        serialized_questions.append({
            'id': question.id,
            'text': question.question_text,
            'answers': [
                {'id': option.id, 'text': option.option_text}
                for option in question.answer_options
            ]
        })
    return render_template('tests/take_test.html',
                            title='Take Test',
                            test=test,
                            questions=serialized_questions)

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
