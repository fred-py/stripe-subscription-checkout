import os
from flask_migrate import upgrade
from app import create_app  # db
#from app.models import CustomerDB, Address, Bin, Subscription, Invoice
from dotenv import load_dotenv, find_dotenv

# Setup Stripe python client library
load_dotenv(find_dotenv())
# Create app instance
# export FLASK_CONFIG=production/development/testing
# NOTE: Add FLASK_CONFIG to FL0 environment variables
app = create_app(os.getenv('FLASK_CONFIG') or 'default')

if __name__ == '__main__':
    app.run()
