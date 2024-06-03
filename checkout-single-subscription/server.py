import os
import click
from flask_migrate import upgrade
from app import create_app, db
#from app.models import CustomerDB, Address, Bin, Subscription, Invoice
from dotenv import load_dotenv, find_dotenv
from app.models import User, Role, CustomerDB, \
    Address, Bin, Subscription, Invoice
from app.query_ops import CustomerQuery, BinQuery

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
    return dict(
        db=db, User=User, Role=Role,
        CustomerDB=CustomerDB, Address=Address,
        Bin=Bin, Subscription=Subscription,
        Invoice=Invoice, CustomerQuery=CustomerQuery,
        BinQuery=BinQuery
    )


@app.cli.command()  # The cli.command decorator simplifies the implementation of custom commands
@click.argument('test_names', nargs=-1)
def test(test_names, pytest=None):
    """Run the unit tests.
    To run on shell:
    $ export FLASK_APP=server.py
    $ flask test """

    import unittest
    if test_names:
        tests = unittest.TestLoader().loadTestsFromNames(test_names)
    else:
        tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)



if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0')
