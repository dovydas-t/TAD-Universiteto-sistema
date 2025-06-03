from flask_wtf import FlaskForm
from app.forms.test_question_form import TestQuestionForm
from wtforms import SelectField, SubmitField, TextAreaField, HiddenField,StringField,FieldList, FormField
from wtforms.validators import DataRequired, Optional, Length


class TestForm(FlaskForm):

    name = StringField()
    module_id = SelectField(
        'Module: ', 
        coerce=int, 
        validators=[DataRequired(message="Please select a Module")]
    )
    
    submit = SubmitField('SaveTest')