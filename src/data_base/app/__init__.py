# https://www.digitalocean.com/community/tutorials/how-to-structure-a-large-flask-application-with-flask-blueprints-and-flask-sqlalchemy
""" This file holds code for **Flask factory function** 
This function is used to set and create the Flask app instance
where all Flask blueprints are linked together, 
combined into one application"""


# Importing necessary modules
from flask import Flask
from config import Config
from app.extensions import db


# Creating the Flask application factory function
def create_app(config_class=Config):
    app = Flask(__name__)  # Creating the Flask app instance
    app.config.from_object(config_class)  # Loading configuration from the Config class

    # Initialize Flask extensions here
    db.init_app(app)  # Initializing the SQLAlchemy database extension

    # Register blueprints here
    # Blueprints are located in the main directory
    from app.main import bp as main_bp
    # Registering the main blueprint for Flask to treat it as part of the application
    app.register_blueprint(main_bp)

    from app.users import bp as users_bp
    app.register_blueprint(users_bp)

    # Defining a test route
    @app.route('/test/')
    def test_page():
        return '<h1>Testing the Flask Application Factory Pattern</h1>'

    return app  # Returning the Flask app instance

