from flask import Blueprint
bp = Blueprint('shelter', __name__, url_prefix='/shelter')
from . import routes
