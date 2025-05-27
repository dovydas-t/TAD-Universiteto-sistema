from flask_admin import Admin
from .views import RegistrationRequestView, QuickActionsView
from .dashboard import AdminDashboardView

def create_admin(app):
    """
    Initialize Flask-Admin with proper organization
    """
    admin = Admin(
        app, 
        name='Registration Admin', 
        template_mode='bootstrap3',
        index_view=AdminDashboardView(name='Dashboard')
    )
    
    # Add views from separate modules
    admin.add_view(RegistrationRequestView(name='Registration Requests'))
    admin.add_view(QuickActionsView(name='Quick Actions'))
    
    # Optional: Add other model management
    from .views import StudyProgramView, ModuleView, UserView
    admin.add_view(StudyProgramView(name='Study Programs'))
    admin.add_view(ModuleView(name='Modules')) 
    admin.add_view(UserView(name='Users'))
    
    return admin