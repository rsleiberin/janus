# app/blueprints/home/routes.py

from flask import render_template, current_app
from . import home

@home.route('/hometest')
def hometest():
    current_app.logger.debug('Home test route is being called')
    return 'Home test route works!'

@home.route('/')
def index():
    current_app.logger.debug('Index route is being called')
    try:
        return render_template('index.html')
    except Exception as e:
        current_app.logger.error('Error in index route: {}'.format(e))
        raise e