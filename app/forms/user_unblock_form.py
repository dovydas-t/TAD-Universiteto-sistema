from flask_wtf import FlaskForm
from wtforms import SubmitField

class UnblockUserForm(FlaskForm):
    submit = SubmitField('Unblock')