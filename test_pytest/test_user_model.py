import pytest
from flask import jsonify

from app.extensions import db  # Assuming this is your database setup
from app.models import CustomerDB, User  # Model for the CustomerDB table
from app import create_app


# RUN SPECIFIC METHODS
# $ pytest file_name.py::mode_name_here


TEST_CUSTOMERS = [
    {'name': 'John Doe', 'phone': '555-1234', 'email': 'john@example.com', 'cus_id': 'cus_123', 'paymentintent_id': 'pi_123', 'active': True},  # Active order
    {'name': 'Jane Smith', 'phone': '555-5678', 'email': 'jane@example.com', 'cus_id': 'cus_456', 'paymentintent_id': 'pi_456', 'active': False}  # Inactive order
]

class TestAPI:
    # This decoratos is used to set up state or objects
    # Eg. helper functions to help run the tests,
    # Note that the decorated functions will not
    # run as test themselves
    @pytest.fixture
    def app(self):
        app = create_app('testing')

        with app.app_context():
            db.create_all()
            for customer_data in TEST_CUSTOMERS:
                customer = CustomerDB(**customer_data)
                db.session.add(customer)
            db.session.commit()

        yield app

        with app.app_context():
            db.session.remove()
            db.drop_all()
    
    @pytest.fixture
    def client(self, app):
        return app.test_client()

    def test_verify_auth_token(self, app):
        with app.app_context():
            user = User(
                email='test@test.com',
                password='Testdopa9wdjwoia9jdwoalij'
            )
            db.session.add(user)
            db.session.commit()
            auth_token = user.generate_auth_token(user.id)
            assert (isinstance(auth_token, str))
            assert (User.verify_auth_token(auth_token), User)