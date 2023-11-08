# app/__init__.py
from flask import Flask

def create_app():
    app = Flask(__name__)

    with app.app_context():
        # Import the blueprint within the application context to avoid any out of context issues
        from app.blueprints.home.routes import home
        app.register_blueprint(home)
        app.logger.debug('Registered home blueprint with app context')

    return app