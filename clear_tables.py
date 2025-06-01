from app import create_app, db
from app.models.faculty import Faculty
from app.models.study_program import StudyProgram
from app.models.module import Module
from app.models.auth import AuthUser
from app.models.profile import UserProfile
from sqlalchemy import text  # <-- Add this import

try:
    app = create_app()

    with app.app_context():
        db.session.execute(text('DELETE FROM module'))
        db.session.execute(text('DELETE FROM user_profile'))  # <-- Delete user_profile first
        db.session.execute(text('DELETE FROM `groups`'))      # <-- Then groups
        db.session.execute(text('DELETE FROM study_program'))
        db.session.execute(text('DELETE FROM faculty'))
        db.session.execute(text('DELETE FROM auth_fluser'))
        db.session.commit()
        print("All data deleted from module, user_profile, groups, study_program, faculty, and authuser tables.")
except Exception as e:
    print(f"{e}")