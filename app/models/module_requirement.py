from app.extensions import db

class ModuleRequirement(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'))
    required_module_id = db.Column(db.Integer, db.ForeignKey('module.id'))

    module = db.relationship("Module", foreign_keys=[module_id], back_populates="requirements")
    required_module = db.relationship("Module", foreign_keys=[required_module_id], back_populates="required_for")
