from app.extensions import db
from app.models.enum import RoleEnum
from app.models.enrolled_modules import enrolled_modules
from app.models.completed_modules import completed_modules

class UserProfile(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('auth_user.id'), primary_key=True)

    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    birth_date = db.Column(db.Date, nullable=True)
    age = db.Column(db.Integer)
    email = db.Column(db.String(35), unique=True, nullable=True)
    failed_logins = db.Column(db.Integer)

    profile_pic_path = db.Column(db.String(255))


    is_active = db.Column(db.Boolean, default=True)
    study_program_id = db.Column(db.Integer, db.ForeignKey('study_program.id'), nullable=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))

    #user role setting
    role = db.Column(db.Enum(RoleEnum), default=RoleEnum.Student, nullable=False)

    #Account creation time
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)

    #Last acc update time
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    #FIXME: need to be changed to last_activity, because, its what it is doing now...
    #TODO: rename this to last activity
    last_login = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp(), nullable=False)

    #Relationships
    user = db.relationship('AuthUser', back_populates='profile')
    study_program = db.relationship("StudyProgram", back_populates="users")
    group = db.relationship("Groups", back_populates="users")
    attendances = db.relationship("Attendance", back_populates="student")
    grades = db.relationship("Grade", back_populates="student")
    schedule_items = db.relationship("ScheduleItem", back_populates="user")
    modules = db.relationship(
        'Module',
        secondary=enrolled_modules,
        backref='enrolled_users'
    )
    completed_modules = db.relationship(
        'Module',
        secondary=completed_modules,
        backref='completed_by_users'
    )
 
    
    def __init__(self, role=RoleEnum.Student, **kwargs):
        super(UserProfile, self).__init__(**kwargs)
        self.role = role

    def __repr__(self):
        return f"UserProfile('{self.id}', '{self.created_at}')"

    @property
    def full_name(self):
        """Get user's full name"""  
        return f"{self.first_name or ''} {self.last_name or ''}".strip() or self.user.username

    

