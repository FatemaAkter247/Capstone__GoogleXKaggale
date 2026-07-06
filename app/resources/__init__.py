from flask import Blueprint
bp = Blueprint('resources', __name__, url_prefix='/resources')
from . import routes
