from app.models.schedule_item import ScheduleItem
from app.extensions import db

class ScheduleService:
    @staticmethod
    def add_module_sessions_to_schedule(user_profile, module):
        for session in module.sessions:
            # Check for conflicts
            conflict = ScheduleItem.query.filter(
                ScheduleItem.user_id == user_profile.id,
                ScheduleItem.date == session.date
            ).first()
            if conflict:
                continue  # Or handle as needed

            schedule_item = ScheduleItem(
                user_id=user_profile.id,
                module_id=module.id,
                type=session.type,
                date=session.date
            )
            db.session.add(schedule_item)
        db.session.commit()