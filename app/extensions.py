# https://www.digitalocean.com/community/tutorials/how-to-structure-a-large-flask-application-with-flask-blueprints-and-flask-sqlalchemy#creating-a-file-for-managing-flask-extensions-and-integrating-flask-sqlalchemy
"""
Extensions are created in this file.
The db object will be used to integrate SQLAlchemy with the 
Flask application constructed in the factory function in:
app/__init__.py """

from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_migrate import Migrate
from flask_mail import Mail, Message
from flask_login import LoginManager
#from app.db_operations.query_ops import CustomerQuery, BinQuery


# Create database object with no arguments
db = SQLAlchemy()
bootstrap = Bootstrap()  # For bootstrap integration
#cus_query = CustomerQuery()  # For customer query
#bin_query = BinQuery()  # For bin query
# flask_moment is an extension that makes 
# it easy to work with moment.js and time
# moment.js is a JavaScript library that renders
# dates and times in the browser by accessing locale settings in the user's computer
moment = Moment()  # For time integration
migrate = Migrate()  # For database migration
mail = Mail()  # For email integration
login_manager = LoginManager()  # For user authentication
