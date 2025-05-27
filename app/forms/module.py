from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SelectField, FileField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange
from app.models.enum import SemesterEnum

class ModuleForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(max=255)])
    description = TextAreaField("Description", validators=[DataRequired()])
    credits = IntegerField("Credits", validators=[DataRequired(), NumberRange(min=1, max=60)])
    
    semester = SelectField(
        "Semester",
        choices=[(sem.name, sem.value) for sem in SemesterEnum],
        validators=[DataRequired()]
    )
    
    study_program_id = SelectField("Study Program", coerce=int, validators=[DataRequired()])
    
    image_path = FileField("Image")  # Use Flask-Uploads or Flask-Dropzone to handle file saving
    
    submit = SubmitField("Save")

    def set_study_program_choices(self, study_programs):
        """Dynamically populate choices."""
        self.study_program_id.choices = [(sp.id, sp.name) for sp in study_programs]
