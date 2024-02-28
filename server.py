import os
from flask_migrate import upgrade
from app import create_app, db
#from app.models import CustomerDB, Address, Bin, Subscription, Invoice
from dotenv import load_dotenv, find_dotenv
from app.models import User, Role

# Setup Stripe python client library
load_dotenv(find_dotenv())
# Create app instance
# export FLASK_CONFIG=production/development/testing
# NOTE: Add FLASK_CONFIG to FL0 environment variables
app = create_app(os.getenv('FLASK_CONFIG') or 'default')


@app.shell_context_processor
def make_shell_context():
    """This function adds the
    database instance and models
    to the flask shell context"""
    return dict(db=db, User=User, Role=Role)


if __name__ == '__main__':
    app.run()
