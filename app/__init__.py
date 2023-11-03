from flask import Flask

def create_app():
    app = Flask(__name__)

    # Later, here you can register blueprints, initialize extensions, etc.

    return app
