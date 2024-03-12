# https://www.digitalocean.com/community/tutorials/how-to-structure-a-large-flask-application-with-flask-blueprints-and-flask-sqlalchemy
# Page 110-116 of Flask Web Development 2nd Edition
""" This file holds code for **Flask factory function** 
This function is used to set and create the Flask app instance
where all Flask blueprints are linked together, 
combined into one application"""

from flask import Flask
from config import config
from app.extensions import db, bootstrap, moment, migrate, mail, login_manager
    # cus_query, bin_query
from dotenv import load_dotenv, find_dotenv

# Setup Stripe python client library
load_dotenv(find_dotenv())
# The login view is the endpoint for login
# Because the route is inside a bp, it needs to be prefixed with the blueprint name
login_manager.login_view = 'auth.login'


def create_app(config_name='production'):  # Change to 'production' before deployment
    """Flask application factory function configuration
    settings stored in one of the classes defined in
    config.py can be imported directly into the app using 
    the from_object() method of the app.config
    configuration object"""
    app = Flask(
        __name__,
        static_folder='static',
        static_url_path='',
        template_folder='templates',
    )
    # config is a dictionary that holds the different configurations for the app
    
    # Create an instance of Config class / config dict contains the different configurations
    config_class = config[config_name]
    app.config.from_object(config_class())  
    #app.config.from_object(config[config_name])  # Loading configuration from the Config class
    config[config_name].init_app(app)

    # Initialize Flask extensions here
    db.init_app(app)  # SQLAlchemy database extension
    #cus_query.init_app(app)  # Customer query extension
    #bin_query.init_app(app)  # Bin query extension
    bootstrap.init_app(app)
    moment.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    login_manager.init_app(app)

    # Register blueprints here
    from .main import main as main_bp  # Main refers to Stripe BP
    app.register_blueprint(main_bp)

    from .db_views import db_views as db_views_bp  # DB front-end  # Passing the app configuration to the blueprint
    app.register_blueprint(db_views_bp)

    from .auth import auth as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth') # prefix adds /auth to all routes in the blueprint

    from .customers import customers as customers_bp
    app.register_blueprint(customers_bp)

    #from app.users import bp as users_bp
    #app.register_blueprint(users_bp)

    #from app.models import bp as models_bp
    #app.register_blueprint(models_bp)

    # Attached routes and custome error pages here

    # Defining a test route
    #@app.route('/test/')
    #def test_page():
    #    return '<h1>Testing the Flask Application Factory Pattern</h1>'

    return app  # Returning the Flask app instance
