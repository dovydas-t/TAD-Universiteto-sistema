from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, SelectField, SelectMultipleField ,ValidationError 
from wtforms.validators import Length, Email, Optional, DataRequired
from flask_login import current_user
from app.models.study_program import StudyProgram
from app.models.module import Module
from app.models.module_requirement import ModuleRequirement
from app.utils.validators import ModuleRequirementsValidator


class RegistrationtoStudiesForm(FlaskForm):
    study_program_id = SelectField('Studies Programs: ', coerce=int, validators=[DataRequired()])
    study_module_id = SelectMultipleField(
        'Select Modules:', 
        coerce=int, 
        validators=[
            DataRequired(message="Please select at least one module"), ModuleRequirementsValidator(
                message="Cannot register for '{module_name}'. Missing prerequisites: {missing_modules}"
            )

        ]
    )


    def __init__(self, *args, **kwargs):
        super(RegistrationtoStudiesForm, self).__init__(*args, **kwargs)
        
        # study programs from database(from database)
        self.study_program_id.choices = [(s.id, s.name) for s in StudyProgram.query.all()]
        # study modules from database(from database)
        self.study_module_id.choices = [(module.id, module.name) for module in Module.query.all()]

        
        # # Model radio buttons (from database)
        # self.model_id.choices = [(model.id, f"{model.model_name} ({model.manufacture_year.year})") 
        #                         for model in Model.query.join(ManufactureYear).all()]
        
        # # Color dropdown (from database)
        # self.color_id.choices = [(color.id, color.color_name) for color in Color.query.all()]