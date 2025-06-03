from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, RadioField ,SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.models.auth import AuthUser
from app.utils.validators import StrongPassword
from app.services.study_program_service import StudyProgramService
from app.models.enum import RoleEnum


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    role = RadioField('I am registering as:', 
                     choices=[
                         ('Student', 'Student'),      # Match your enum values
                         ('Teacher', 'Teacher')
                     ],
                     default='Student',               # Default to 'Student'
                     validators=[DataRequired()])
    
    # Conditional fields
    study_program_id = SelectField('Study Program', coerce=int)
    registration_code = StringField('Teacher Registration Code')
    
    password = PasswordField('Password', validators=[DataRequired(),StrongPassword()])
    password2 = PasswordField('Confirm Password', 
                             validators=[DataRequired(), StrongPassword(), EqualTo('password')])
    submit = SubmitField('Register')
    
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        # Populate study programs
        self.study_program_id.choices = [(0, 'Select Study Program')] + \
            [(p.id, p.name) for p in StudyProgramService.get_all_study_programs()]
    
    def validate_study_program_id(self, field):
        if self.role.data == 'Student':  # Use 'Student' (capitalized)
            if not field.data or field.data == 0:
                raise ValidationError('Study program is required for students.')

    def validate_registration_code(self, field):
        if self.role.data == 'Teacher':  # Use 'Teacher' (capitalized)
            if not field.data or field.data != 'TEACH2024':
                raise ValidationError('Valid teacher registration code is required.')
    
    def validate_username(self, username):
        user = AuthUser.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists.')
    

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

#FIXME:Profile related form should be inside: forms/main.py
class UpdateProfileForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(), 
        Length(min=4, max=25)
    ])
    first_name = StringField('First Name', validators=[Length(max=50)])
    last_name = StringField('Last Name', validators=[Length(max=50)])
    
    study_program_id = SelectField(
        'Study Program:', 
        coerce=int, 
        validators=[DataRequired(message="Please select a study program")]
    )
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[
        DataRequired(), 
        EqualTo('password', message='Passwords must match')
    ])
    submit = SubmitField('Update Pr')



# Flask-WTF automatically calls custom validators during form.validate_on_submit()
# Any method named validate_<fieldname> gets executed after built-in validators pass
# If ValidationError is raised, form validation fails and error shows in template
    # def validate_username(self, username):
    #     user = AuthUser.query.filter_by(username=username.data).first()
    #     if user:
    #         raise ValidationError('Username already exists.')

    # def validate_email(self, email):
    #     user = AuthUser.query.filter_by(email=email.data).first()
    #     if user:
    #         raise ValidationError('Email already registered.')

#FIXME:Profile related form should be inside: forms/main.py
class EnterEmailForm(FlaskForm):
    """Enter email to request password reset"""
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

class PasswordForm(FlaskForm):
    """Form for user to enter his password 2 times"""
    password = PasswordField('Enter Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[
        DataRequired(), 
        EqualTo('password', message='Passwords must match')
    ])
    submit = SubmitField('Submit Password')
