from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.models.auth import AuthUser


class RegistrationForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField('Password',validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Repeat Password', validators=[
        DataRequired(), 
        EqualTo('password', message='Passwords must match')
    ])
    submit =SubmitField('Register')

    def validate_username(self, username):
        user = AuthUser.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class UpdateProfileForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(), 
        Length(min=4, max=25)
    ])
    first_name = StringField('First Name', validators=[Length(max=50)])
    last_name = StringField('Last Name', validators=[Length(max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[
        DataRequired(), 
        EqualTo('password', message='Passwords must match')
    ])
    submit = SubmitField('Register')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Create Post')
    

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
