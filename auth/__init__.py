from flask import Blueprint

# create blueprint
auth = Blueprint('auth', __name__)

# import the routes associated with this blueprint
from . import routes