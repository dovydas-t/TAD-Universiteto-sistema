from app.extensions import db
from app.models.enum import SemesterEnum

class Module(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    description = db.Column(db.Text)
    credits = db.Column(db.Integer)
    semester = db.Column(db.Enum(SemesterEnum))
    study_program_id = db.Column(db.Integer, db.ForeignKey('study_program.id'))
    image_path = db.Column(db.String(255))

    study_program = db.relationship("StudyProgram", back_populates="modules")

    requirements = db.relationship("ModuleRequirement", 
                                 foreign_keys='ModuleRequirement.module_id', 
                                 back_populates="module")
    
    required_for = db.relationship("ModuleRequirement", 
                                foreign_keys='ModuleRequirement.required_module_id', 
                                back_populates="required_module")
    
    assignments = db.relationship("Assignment", back_populates="module")
    tests = db.relationship("Test", back_populates="module")
    attendances = db.relationship("Attendance", back_populates="module")
    grades = db.relationship("Grade", back_populates="module")
    schedule_items = db.relationship("ScheduleItem", back_populates="module")
    sessions = db.relationship("Session", back_populates="module")