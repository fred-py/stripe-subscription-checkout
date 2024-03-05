import os
from dotenv import load_dotenv, find_dotenv
basedir = os.path.abspath(os.path.dirname(__file__))

load_dotenv(find_dotenv())


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')  # flask-wtf 
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.googlemail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', '587'))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'true').lower() in \
        ['true', 'on', '1']
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    UNITED_MAIL_SUBJECT_PREFIX = '[United]'
    UNITED_MAIL_SENDER = 'United Admin <pythonapi2023@gmail.com>'
    UNITED_ADMIN = os.getenv('UNITED_ADMIN')
    UNITED_ADMIN_1 = os.getenv('UNITED_ADMIN_1')
    UNITED_ADMIN_2 = os.getenv('UNITED_ADMIN_2')
    UNITED_ADMIN_3 = os.getenv('UNITED_ADMIN_3')
    UNITED_DRIVER = os.getenv('UNITED_DRIVER')
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PORT = int(os.getenv('PORT', 4242))  # This is needed to deploy on fl0
    
    @staticmethod
    def init_app(app):
        pass


# Different configurations for the app to run in different environments
class DevelopmentConfig(Config):
    DEBUG = True

    def __init__(self):
        self.SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')


class TestingConfig(Config):
    TESTING = True

    def __init__(self):
        self.SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


class ProductionConfig(Config):
    DEBUG = False
    # Assignment of the database URL to the SQLALCHEMY_DATABASE_URI
    # This has been moved into the __init__ method
    # Tis class definition was running before env variables were loaded
    # Now in create_app() function, an instance of the Config class is created
    
    def __init__(self):
        self.SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig,
}
