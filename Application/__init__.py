from flask import Flask
import secrets
from .dbmanager import get_db

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY=secrets.token_urlsafe(32))
    
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
    
    app.teardown_appcontext(cleanup)
    make_blueprints(app)
    
    from .dbmanager import init_db_command
    app.cli.add_command(init_db_command)
    
    return app
    
def make_blueprints(app):
    from .blueprints.home_view import bp as home_bp
    from .blueprints.competencies_view import bp as competencies_bp
    from .blueprints.course_view import bp as course_bp
    from .blueprints.courses_view import bp as courses_bp
    from .blueprints.domains_view import bp as domains_bp
    app.register_blueprint(home_bp)
    app.register_blueprint(competencies_bp)
    app.register_blueprint(course_bp)
    app.register_blueprint(courses_bp)
    app.register_blueprint(domains_bp)
    
def cleanup(value):
    get_db().close()