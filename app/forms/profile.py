from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, ValidationError
from wtforms.validators import Length, Email, Optional
from app.models.auth import AuthUser
from app.models.profile import UserProfile

from flask_login import current_user



class ProfileForm(FlaskForm):
    username = StringField('Username',validators=[Length(min=3, max=20), Optional()])
    first_name = StringField('First Name', validators=[Length(max=50), Optional()])
    last_name = StringField('Last Name', validators=[Length(max=50), Optional()])
    email = StringField('Email', validators=[Length(min=6, max=35), Email(), Optional()])
    birth_date = DateField('Birth Date (YYYY-MM-DD)', format='%Y-%m-%d', validators=[Optional()])
    submit = SubmitField('Update Profile')

#Functions execute when from is being submitted
    def validate_username(self, field):
        if field.data != current_user.username:
            username = AuthUser.query.filter_by(username=field.data).first()
            if username:
                raise ValidationError("Username already exists.")

    def validate_email(self, email_field):
        if email_field.data != current_user.profile.email:
            user = UserProfile.query.filter_by(email=email_field.data).first()
            if user:
                raise ValidationError('Email is already in use.')