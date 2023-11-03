from flask import Blueprint

design = Blueprint('design', __name__)

from . import routes
