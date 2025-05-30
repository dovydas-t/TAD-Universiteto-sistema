from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, SubmitField
from wtforms.validators import DataRequired, Optional, Email, Length
from app.services.study_program_service import StudyProgramService
from app.services.group_service import GroupsService

class StudentEditForm(FlaskForm):
    first_name = StringField("First Name", validators=[Optional(), Length(max=64)])
    last_name = StringField("Last Name", validators=[Optional(), Length(max=64)])
    birth_date = DateField("Birth Date", validators=[Optional()], format='%Y-%m-%d')
    email = StringField("Email", validators=[Optional(), Email(), Length(max=35)])
    
    study_program_id = SelectField("Study Program", coerce=int, validators=[Optional()])
    group_id = SelectField("Group", coerce=int, validators=[Optional()])
    
    submit = SubmitField("Save Changes")

    def __init__(self, *args, **kwargs):
        super(StudentEditForm, self).__init__(*args, **kwargs)
        
        # Populate dropdowns
        self.study_program_id.choices = StudyProgramService.get_dropdown_choices()
        self.group_id.choices = GroupsService.get_dropdown_choices()
