"""auth relates to the database authentication
process for internal use only."""

from flask import Blueprint

auth = Blueprint('auth', __name__)

from . import views