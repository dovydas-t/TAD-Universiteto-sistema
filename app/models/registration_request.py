from app.extensions import datetime , db


class RegistrationRequest(db.Model):
    """
    Model to store student registration requests that need admin approval
    
    This table stores requests when the RegistrationDecisionEngine determines
    that a registration cannot be processed immediately and needs admin review.
    """
    __tablename__ = 'registration_request'
    
    # Primary key
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Foreign keys linking to other tables
    student_id = db.Column(db.Integer, db.ForeignKey('user_profile.id'), nullable=False)
    study_program_id = db.Column(db.Integer, db.ForeignKey('study_program.id'), nullable=False)
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'), nullable=False)
    
    # Request status and workflow fields
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    reason = db.Column(db.String(200))  # Why approval is needed (from decision engine)
    
    # Notes from student and admin
    student_notes = db.Column(db.Text)  # Student's explanation/request
    admin_notes = db.Column(db.Text)    # Admin's decision notes
    
    # Admin who processed the request
    admin_id = db.Column(db.Integer, db.ForeignKey('user_profile.id'))
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    processed_at = db.Column(db.DateTime)  # When admin made decision
    
    # Relationships to other models
    student = db.relationship("UserProfile", foreign_keys=[student_id], backref="registration_requests")
    study_program = db.relationship("StudyProgram", backref="registration_requests") 
    module = db.relationship("Module", backref="registration_requests")
    admin = db.relationship("UserProfile", foreign_keys=[admin_id])

    def __repr__(self):
        return f'<RegistrationRequest {self.id}: {self.student.first_name if self.student else "Unknown"} -> {self.module.name if self.module else "Unknown"}>'
