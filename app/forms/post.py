from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, ValidationError, TextAreaField
from wtforms.validators import Length, DataRequired

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Create Post')