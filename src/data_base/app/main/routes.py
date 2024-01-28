"""Holds routes for main blueprint
For Flask to use these routes and to make them 
importable directly from the blueprint,
routes.py file must be imported into 
blueprint's  __init__.py file in main directory."""

from flask import render_template
from app.main import bp

@bp.route('/')  # This is similar to app.route('/')
def index():
    return render_template('index.html')
