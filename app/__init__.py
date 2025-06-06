from flask import Flask
from flask_login import user_logged_in
from app.extensions import db, migrate, login_manager, csrf, random
from app.config import Config
from app.models.auth import AuthUser


def jinja_random():
        return random.randint(0, 999999)

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.jinja_env.globals['random'] = jinja_random
    app.config['UPLOAD_FOLDER'] = 'app/static'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)


    # Register user loader
    @login_manager.user_loader
    def load_user(user_id):
        user = AuthUser.query.get(int(user_id))
        if user:
            #TODO: manau reiketu, padaryti jog cia nustatytu user.profile.last_activity, o last_login dali perkelti i views
            user.profile.last_login = db.func.current_timestamp()
            db.session.commit()
        return user

    # Register blueprints
    from app.views.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    from app.views.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    from app.views.dashboard import bp as dashboard_bp
    app.register_blueprint(dashboard_bp)
    
    from app.views.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    from app.views.study_program import bp as study_program_bp
    app.register_blueprint(study_program_bp, url_prefix='/programs')

    from app.views.profile import bp as profile_bp
    app.register_blueprint(profile_bp, url_prefix='/profile')

    from app.views.student import bp as student_bp
    app.register_blueprint(student_bp, url_prefix='/student')

    from app.views.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

    from app.views.faculty import bp as faculty_bp
    app.register_blueprint(faculty_bp, url_prefix='/faculty')

    from app.views.module import bp as module_bp
    app.register_blueprint(module_bp, url_prefix='/module')

    from app.views.teacher import bp as teacher_bp
    app.register_blueprint(teacher_bp, url_prefix='/teacher')

    from app.views.groups import bp as groups_bp
    app.register_blueprint(groups_bp, url_prefix='/groups')

    from app.views.tests import bp as tests_bp
    app.register_blueprint(tests_bp, url_prefix='/test')

    from app.views.test_question import bp as test_question_bp
    app.register_blueprint(test_question_bp, url_prefix="/test_question")

    from app.views.grades import bp as grades_bp
    app.register_blueprint(grades_bp, url_prefix="/grades")

    from app.views.users import bp as users_bp
    app.register_blueprint(users_bp, url_prefix='/users')
    
    from app.views.session import bp as session_bp
    app.register_blueprint(session_bp, url_prefix='/session')


    @app.context_processor
    def inject_breadcrumbs():
        from flask import request
        # Get the current URL path and split it
        path = request.path.strip('/').split('/')
        # Create breadcrumb parts
        breadcrumbs = [{'name': 'Home', 'url': '/'}]
        if path != ['']:
            for i in range(len(path)):
                name = path[i].replace('-', ' ').capitalize()
                url = '/' + '/'.join(path[:i + 1])
                breadcrumbs.append({'name': name, 'url': url})
        return dict(breadcrumbs=breadcrumbs)

    return app