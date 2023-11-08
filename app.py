# app.py at the root of your Flask application (~/janus/app.py)
import logging
from app import create_app

app = create_app()

if __name__ == '__main__':
    # Set up logging to the console at a DEBUG level
    app.logger.setLevel(logging.DEBUG)
    # Start the Flask application with detailed logging
    app.run(debug=True)