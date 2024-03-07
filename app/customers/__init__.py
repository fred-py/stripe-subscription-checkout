"""auth relates to the database authentication
process for internal use only."""

from flask import Blueprint

customers = Blueprint('customers', __name__)

from . import views