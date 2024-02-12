"""Creates main blueprint and renders its templates"""
# Page 118 of Flask Web Development Book

from flask import Blueprint

main = Blueprint('main', __name__)

# modules are imported at the bottom of the app/main/__init__.py 
# script to avoid errors due to circular dependencies”
from .import views, errors