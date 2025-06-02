from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, DateTimeField, SubmitField
from wtforms.validators import DataRequired

class SessionForm(FlaskForm):
    module_id = SelectField("Module", coerce=int, validators=[DataRequired()])
    type = StringField("Session Type", validators=[DataRequired()])  # e.g., Lecture, Lab
    date = DateTimeField("Date & Time", format="%Y-%m-%dT%H:%M", validators=[DataRequired()])
    submit = SubmitField("Add Session")