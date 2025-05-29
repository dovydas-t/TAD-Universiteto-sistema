from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, SelectField, ValidationError
from wtforms.validators import Length, Email, Optional, DataRequired
from app.models.auth import AuthUser
from app.models.profile import UserProfile
from app.services.study_program_service import StudyProgramService
from flask_login import current_user



class ProfileForm(FlaskForm):
    username = StringField('Username',validators=[Length(min=3, max=20), Optional()])
    first_name = StringField('First Name', validators=[Length(max=50), Optional()])
    last_name = StringField('Last Name', validators=[Length(max=50), Optional()])
    email = StringField('Email', validators=[Length(min=6, max=35), Email(), Optional()])
    birth_date = DateField('Birth Date (YYYY-MM-DD)', format='%Y-%m-%d', validators=[Optional()])
    
    study_program_id = SelectField(
        'Study Program:', 
        coerce=int, 
        validators=[DataRequired(message="Please select a study program")]
    )
    
    submit = SubmitField('Update Profile')

    
    def __init__(self, user=None, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.study_program_id.choices = [(sp.id, sp.name) for sp in StudyProgramService.get_all_study_programs()]
    # FIXME Palikti sita dali init arba perkelti i route
        if user:
            self.study_program_id.data = user.profile.study_program_id

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
    