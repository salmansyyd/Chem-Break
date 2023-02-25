
from flask import Blueprint

auth = Blueprint('auth', __name__)


def import_routes():
    from . import routes


import_routes()
