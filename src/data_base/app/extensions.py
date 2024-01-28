# https://www.digitalocean.com/community/tutorials/how-to-structure-a-large-flask-application-with-flask-blueprints-and-flask-sqlalchemy#creating-a-file-for-managing-flask-extensions-and-integrating-flask-sqlalchemy
"""The db object will be used to integrate SQLAlchemy with the 
Flask application constructed in the factory function in:
app/__init__.py """

from flask_sqlalchemy import SQLAlchemy
# Create db object with no arguments
db = SQLAlchemy()