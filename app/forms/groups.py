from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, StringField, SubmitField, SelectMultipleField
from wtforms.validators import DataRequired, NumberRange, Optional
from wtforms.widgets import ListWidget, CheckboxInput

class GroupForm(FlaskForm):
    study_program_id = SelectField('Study Program', coerce=int, validators=[DataRequired()])
    starting_year = IntegerField('Starting Year', validators=[DataRequired(), NumberRange(min=2000, max=2025)])
    code = StringField('Group Code', render_kw={'readonly': True})  # readonly so user cannot edit
    submit = SubmitField('Create Group')

class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()

class EditGroupForm(FlaskForm):
    teacher_id = SelectField('Teacher', coerce=int, validators=[Optional()])
    students = MultiCheckboxField('Students', coerce=int)
    submit = SubmitField('Save Changes')