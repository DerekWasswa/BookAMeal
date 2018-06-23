''' LINK TO THE API Documentation '''
from flask import Blueprint

endpoints_blueprint = Blueprint('doc', __name__)

from .import views
