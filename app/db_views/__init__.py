from flask import Blueprint

db_views = Blueprint('db_views', __name__)

from . import views # views module in db_views package
