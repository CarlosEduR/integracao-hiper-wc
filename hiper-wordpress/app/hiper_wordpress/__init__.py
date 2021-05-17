from flask.blueprints import Blueprint

bp = Blueprint('hiper_wordpress', __name__)

from app.hiper_wordpress.rest import integration_resource
from app.hiper_wordpress.rest import template_resource
from app.hiper_wordpress.rest import auth_resource
from app.hiper_wordpress.rest import customer_resource