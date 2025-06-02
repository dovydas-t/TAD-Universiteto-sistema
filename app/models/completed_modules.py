from app.extensions import db

completed_modules = db.Table(
    'completed_modules',
    db.Column('user_profile_id', db.Integer, db.ForeignKey('user_profile.id'), primary_key=True),
    db.Column('module_id', db.Integer, db.ForeignKey('module.id'), primary_key=True)
)
