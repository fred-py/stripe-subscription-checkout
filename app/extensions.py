# https://www.digitalocean.com/community/tutorials/how-to-structure-a-large-flask-application-with-flask-blueprints-and-flask-sqlalchemy#creating-a-file-for-managing-flask-extensions-and-integrating-flask-sqlalchemy
"""
Extensions are created in this file.
The db object will be used to integrate SQLAlchemy with the 
Flask application constructed in the factory function in:
app/__init__.py """

from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_moment import Moment
#from flask_mail import Mail

# Create database object with no arguments
db = SQLAlchemy()

bootstrap = Bootstrap()  # For bootstrap integration

# flask_moment is an extension that makes 
# it easy to work with moment.js and time
# moment.js is a JavaScript library that renders
# dates and times in the browser by accessing locale settings in the user's computer
moment = Moment()  # For time integration


#mail = Mail()  # For email integration
