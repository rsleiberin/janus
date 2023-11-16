from flask import jsonify, current_app
from . import home

@home.route('/api/home')
def home_data():
    current_app.logger.debug('Home data API route is being called')
    # Example data structure
    home_content = {
        "title": "Welcome to Lodestone",
        "introText": "Discover our unique approach...",
        "projects": [
            {"id": 1, "title": "Project 1", "description": "Description of Project 1"},
            # ... other projects
        ]
    }
    return jsonify(home_content)
