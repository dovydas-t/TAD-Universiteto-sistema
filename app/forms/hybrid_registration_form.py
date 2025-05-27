from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Optional, Length
from app.models.study_program import StudyProgram
from app.models.module import Module


class HybridRegistrationForm(FlaskForm):
    """
    Main registration form for students - handles both immediate and approval cases
    """
    module_id = SelectField(
        'Select Module:', 
        coerce=int, 
        validators=[DataRequired(message="Please select a module")]
        # Note: We don't use validators here since decision engine handles validation
    )
    
    student_notes = TextAreaField(
        'Additional Notes (Optional):',
        validators=[
            Optional(),
            Length(max=300, message="Notes must be less than 300 characters")
        ],
        description="Any special circumstances or requests"
    )
    
    submit = SubmitField('Register for Module')

    def __init__(self, *args, **kwargs):
        super(HybridRegistrationForm, self).__init__(*args, **kwargs)
        
        # Populate module choices
        self.module_id.choices = [('', 'Select a Module')] + [
            (m.id, f"{m.name} ({m.credits} credits)") for m in Module.query.all()
        ]




















# class RegistrationtoStudiesForm(FlaskForm):
#     study_program_id = SelectField('Studies Programs: ', coerce=int, validators=[DataRequired()])
#     study_module_id = SelectMultipleField(
#         'Select Modules:', 
#         coerce=int, 
#         validators=[
#             DataRequired(message="Please select at least one module"), ModuleRequirementsValidator(
#                 message="Cannot register for '{module_name}'. Missing prerequisites: {missing_modules}"
#             )

#         ]
#     )


#     def __init__(self, *args, **kwargs):
#         super(RegistrationtoStudiesForm, self).__init__(*args, **kwargs)
        
#         # study programs from database(from database)
#         self.study_program_id.choices = [(s.id, s.name) for s in StudyProgram.query.all()]
#         # study modules from database(from database)
#         self.study_module_id.choices = [(module.id, module.name) for module in Module.query.all()]

        
#         # # Model radio buttons (from database)
#         # self.model_id.choices = [(model.id, f"{model.model_name} ({model.manufacture_year.year})") 
#         #                         for model in Model.query.join(ManufactureYear).all()]
        
#         # # Color dropdown (from database)
#         # self.color_id.choices = [(color.id, color.color_name) for color in Color.query.all()]