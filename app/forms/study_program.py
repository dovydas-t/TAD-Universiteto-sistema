from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField, DateField, ValidationError
from wtforms.validators import Length, DataRequired
from app.models.study_program import StudyProgram
from app.services.faculty_service import FacultyService

class StudyProgramForm(FlaskForm):
    name = StringField('Study Program Name', validators=[DataRequired(), Length(max=255)])
    faculty_id = SelectField('Faculty', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Save')

    def __init__(self, *args, **kwargs):
        super(StudyProgramForm, self).__init__(*args, **kwargs)
        self.faculty_id.choices = [
            (faculty.id, faculty.name) for faculty in FacultyService.get_all_faculties()
        ]