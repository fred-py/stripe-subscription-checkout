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

    def test_get_customers(self, client):
        response = client.get('/api/v1/customers/')
        assert response.status_code == 200
        data = response.get_json()
        assert 'customers' in data
        assert isinstance(data['customers'], list)
        assert len(data['customers']) == 2 

        expected_first_customer = TEST_CUSTOMERS[0]
        first_customer = data['customers'][0]

        assert first_customer['name'] == expected_first_customer['name']
        # ... check other fields as needed

    def test_get_order_stats(self, client):
        response = client.get('/api/v1/orders/')
        assert response.status_code == 200
        data = response.get_json()
        assert 'total_orders' in data
        assert data['total_orders'] == 1  # Only one active order in TEST_CUSTOMERS

    def test_verify_auth_token(self):
        user = User(
            email='test@test.com',
            password='Testdopa9wdjwoia9jdwoalij'
        )
        db.session.add(user)
        db.session.commit()
        auth_token = user.generate_auth_token(user.id)
        assert (isinstance(auth_token, bytes))
        assert (User.decode_auth_token(auth_token) == 1)