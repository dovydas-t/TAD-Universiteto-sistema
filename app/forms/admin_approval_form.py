from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Optional, Length


class AdminApprovalForm(FlaskForm):
    """
    Simple form for admin to approve/reject registration requests
    """
    request_id = HiddenField('Request ID')
    
    decision = SelectField(
        'Decision:',
        choices=[
            ('', 'Select Decision'),
            ('approved', 'Approve Registration'),
            ('rejected', 'Reject Registration')
        ],
        validators=[DataRequired(message="Please select a decision")]
    )
    
    admin_notes = TextAreaField(
        'Admin Notes:',
        validators=[
            Optional(),
            Length(max=500, message="Admin notes must be less than 500 characters")
        ],
        description="Explain your decision (optional)"
    )
    
    submit = SubmitField('Process Request')