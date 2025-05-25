from flask import Flask
from flask_login import user_logged_in
from app.extensions import db, migrate, login_manager, csrf
from app.config import Config
from app.models.auth import AuthUser

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
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
    
    from app.views.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    # from app.views.post import bp as post_bp
    # app.register_blueprint(post_bp, url_prefix='/posts')

    from app.views.profile import bp as profile_bp
    app.register_blueprint(profile_bp, url_prefix='/profile')


    return app