from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, SubmitField, DateField, FileField
from wtforms.validators import DataRequired, Length, Email, ValidationError
from app.services.user_service import UserService


class ProfileSetupForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=50)])
    birth_date = DateField('Birth Date', validators=[DataRequired()])
    profile_picture = FileField('Profile Picture', validators=[
        FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')
    ])
    submit = SubmitField('Complete Profile')

    def validate_email(self, email):
        email = UserService.check_email_exists(email.data)
        if email:
            raise ValidationError('Email is already in use. Please choose a different one.')