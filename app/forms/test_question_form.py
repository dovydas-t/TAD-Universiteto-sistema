from flask_wtf import FlaskForm
from wtforms import StringField, FieldList, FormField, IntegerField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import DataRequired

class AnswerOptionForm(FlaskForm):
    option_text = StringField('Option Text', validators=[DataRequired()])
    is_correct = BooleanField('Is Correct?')

class TestQuestionForm(FlaskForm):
    question_text = TextAreaField('Question Text', validators=[DataRequired()])
    answer_options = FieldList(FormField(AnswerOptionForm), min_entries=4, max_entries=4)
    
    submit = SubmitField('Submit Test question and Answers')