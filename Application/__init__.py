import os
from flask import Flask
import secrets
from .dbmanager import get_db
from flask_login import LoginManager

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=secrets.token_urlsafe(32),
        IMAGE_PATH=os.path.join(app.instance_path, 'images')
    )
    
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
    
    app.teardown_appcontext(cleanup)
    make_blueprints(app)
    
    from .dbmanager import init_db_command
    app.cli.add_command(init_db_command)
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        return get_db().get_user_id(int(user_id))
    
    os.makedirs(app.config['IMAGE_PATH'], exist_ok=True)
    
    return app
    
def make_blueprints(app):
    from .blueprints.home_view import bp as home_bp
    from .blueprints.competencies_view import bp as competencies_bp
    from .blueprints.courses_view import bp as courses_bp
    from .blueprints.domains_view import bp as domains_bp
    app.register_blueprint(home_bp)
    app.register_blueprint(competencies_bp)
    app.register_blueprint(courses_bp)
    app.register_blueprint(domains_bp)
    from .blueprints.auth_views import bp as auth_bp
    app.register_blueprint(auth_bp)
    from .blueprints.elements_view import bp as elements_bp
    app.register_blueprint(elements_bp)
    from .blueprints.profile_views import bp as profile_bp
    app.register_blueprint(profile_bp)
    from .blueprints.members_views import bp as members_bp
    app.register_blueprint(members_bp)
    from .blueprints.user_admins_views import bp as user_admins_bp
    app.register_blueprint(user_admins_bp)
    from .blueprints.admins_views import bp as admins_bp
    app.register_blueprint(admins_bp)
    
def cleanup(value):
    get_db().close()