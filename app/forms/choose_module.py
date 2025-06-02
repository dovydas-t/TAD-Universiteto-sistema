from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField

class ChooseModule(FlaskForm):
    module_id = SelectField('Module', coerce=int)
    submit = SubmitField('Choose')