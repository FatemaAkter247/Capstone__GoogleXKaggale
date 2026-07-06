from flask import Blueprint

bp = Blueprint('citizen', __name__, url_prefix='/citizen')

from . import routes
