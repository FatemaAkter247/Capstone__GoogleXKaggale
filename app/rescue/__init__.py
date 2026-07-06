from flask import Blueprint
bp = Blueprint('rescue', __name__, url_prefix='/rescue')
from . import routes
