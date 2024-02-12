# https://www.digitalocean.com/community/tutorials/how-to-structure-a-large-flask-application-with-flask-blueprints-and-flask-sqlalchemy
# Page 116 of Flask Web Development 2nd Edition
""" This file holds code for **Flask factory function** 
This function is used to set and create the Flask app instance
where all Flask blueprints are linked together, 
combined into one application"""


from flask import Flask
from config import config
from app.extensions import db


# Creating the Flask application factory function
def create_app(config_name='production'):  # Change to 'development' for development
    app = Flask(
        __name__,
        static_folder='static',
        static_url_path='',
        template_folder='template',)
    # config is a dictionary that holds the different configurations for the app
    app.config.from_object(config[config_name])  # Loading configuration from the Config class
    config[config_name].init_app(app)

    # Initialize Flask extensions here
    db.init_app(app)  # Initializing the SQLAlchemy database extension
    #mail.init_app(app)  # Initializing the mail extension

    # Register blueprints here
    # Blueprints are located in the main directory
    #from .main import main as main_bp
    # Registering the main blueprint for Flask to treat it as part of the application
    #app.register_blueprint(main_bp)

    #from app.users import bp as users_bp
    #app.register_blueprint(users_bp)

    #from app.models import bp as models_bp
    #app.register_blueprint(models_bp)

    # Defining a test route
    #@app.route('/test/')
    #def test_page():
    #    return '<h1>Testing the Flask Application Factory Pattern</h1>'

    return app  # Returning the Flask app instance
