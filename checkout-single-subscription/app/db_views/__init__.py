from flask import Blueprint

db_views = Blueprint('db_views', __name__)

from . import views, errors # views module in db_views package
from ..models import Permission

# Adding the Permission class to the template context
@db_views.app_context_processor  # p. 341
def inject_permissions():
    return dict(Permission=Permission)
