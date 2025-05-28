from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, StringField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class GroupForm(FlaskForm):
    study_program_id = SelectField('Study Program', coerce=int, validators=[DataRequired()])
    starting_year = IntegerField('Starting Year', validators=[DataRequired(), NumberRange(min=2000, max=2025)])
    code = StringField('Group Code', render_kw={'readonly': True})  # readonly so user cannot edit
    submit = SubmitField('Create Group')
