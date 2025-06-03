from app.extensions import db

module_teachers = db.Table(
    'module_teachers',
    db.Column('module_id', db.Integer, db.ForeignKey('module.id')),
    db.Column('teacher_id', db.Integer, db.ForeignKey('user_profile.id'))
)