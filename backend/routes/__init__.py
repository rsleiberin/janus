"""
Blueprint registration for the Flask application.
"""

def register_blueprints(app):
    """
    Registers all blueprints for the application.

    Args:
        app (Flask): The Flask application instance.
    """
    from .status_routes import status_bp
    from .file_routes import file_bp
    from .authentication_routes import auth_bp
    from .user_routes import user_bp
    from .admin_routes import admin_bp
    from .error_and_health_monitoring_routes import error_and_health_bp
    from .analytics_routes import analytics_bp
    from .security_routes import security_bp
    from .log_routes import log_bp
    from .image_routes import image_bp

    app.register_blueprint(status_bp)
    app.register_blueprint(file_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(error_and_health_bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(security_bp)
    app.register_blueprint(log_bp)
    app.register_blueprint(image_bp, url_prefix="/images")
