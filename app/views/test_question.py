from flask import Blueprint, flash, request, redirect, render_template, url_for
from flask_login import login_required, current_user
from app.utils.decorators import admin_required
from app.services.test_question_service import TestQuestionService
from app.services.answer_option_service import AnswerOptionService
from app.forms.test_question_form import TestQuestionForm


bp = Blueprint('test_question', __name__)

@bp.route('/detail/<int:test_question_id>')
def detail(test_question_id):
    """Display test question details"""
    test_question = TestQuestionService.get_test_question_by_id(test_question_id)
    
    if not test_question:
        flash('Test has no questions.', 'error')
        return redirect(url_for('test.index'))
    
    return render_template('test_question/test_question_detail.html',
                           title='Test Question Detail',
                           question=test_question)

@bp.route('/add_question/<int:test_id>', methods=['GET', 'POST'])
def add_question(test_id):
    form = TestQuestionForm()

    if form.validate_on_submit():

        question_text = form.question_text.data
        test_question = TestQuestionService.create_and_flush_question(test_id, question_text)


        for answer_form in form.answer_options.entries:
            option_text = answer_form.option_text.data
            is_correct = answer_form.is_correct.data
            AnswerOptionService.create_answer_for_test_question_id(test_question_id=test_question.id,
                                                                                   option_text=option_text,
                                                                                   is_correct=is_correct)

        TestQuestionService.commit_changes()
        flash('Question and answers added successfully!', 'success')
        return redirect(url_for('test.detail', test_id=test_id))
    
    return render_template('test_question/add_question.html', form=form, test_id=test_id)


@bp.route('/edit_question/<int:test_question_id>', methods=['GET', 'POST'])
def edit_question(test_question_id):
    question = TestQuestionService.get_test_question_by_id(test_question_id)
    form = TestQuestionForm(obj=question)

    if form.validate_on_submit():
        try:
            TestQuestionService.update_test_question_from_form(question, form)
            flash('Question updated successfully!')
            return redirect(url_for('test_question.detail', test_question_id=test_question_id))
        except ValueError as e:
            flash(str(e), 'danger')

    return render_template('test_question/edit_question.html', form=form, question=question, test_question_id=test_question_id)
