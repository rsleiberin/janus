# app/blueprints/home/__init__.py
from flask import Blueprint

home = Blueprint('home', __name__, 
                 template_folder='templates', 
                 static_folder='static', 
                 static_url_path='/static/home')

# Remove or comment out: current_app.logger.debug('Home blueprint initialized')