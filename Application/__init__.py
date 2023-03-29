from flask import Flask
import secrets

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY=secrets.token_urlsafe(32))
    
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
    
    app.teardown_appcontext(cleanup)
    make_blueprints(app)
    
    return app
    
def make_blueprints(app:Flask):
    from .blueprints.home_view import bp as home_bp
    app.register_blueprint(home_bp)
    
def cleanup(value):
    pass