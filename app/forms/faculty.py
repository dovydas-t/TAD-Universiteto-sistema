from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class FacultyForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=255)])
    city = StringField('City', validators=[Length(max=100)])
    street = StringField('Street', validators=[Length(max=100)])
    address = StringField('Address', validators=[Length(max=255)])
    description = TextAreaField('Description')
    
    submit = SubmitField('Submit')
