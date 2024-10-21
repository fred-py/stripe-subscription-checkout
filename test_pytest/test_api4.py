import pytest
from flask import jsonify
from app.extensions import db  # Assuming this is your database setup
from app.models import CustomerDB  # Model for the CustomerDB table
from app import create_app  # Assuming you have a factory function for app creation

# Sample Customer data
TEST_CUSTOMERS = [
    {'id': 1, 'name': 'John Doe', 'phone': '555-1234', 'email': 'john@example.com', 'cus_id': 'cus_123', 'paymentintent_id': 'pi_123'},
    {'id': 2, 'name': 'Jane Smith', 'phone': '555-5678', 'email': 'jane@example.com', 'cus_id': 'cus_456', 'paymentintent_id': 'pi_456'}
]

@pytest.fixture
def app():
    app = create_app('testing')
    #app.config['TESTING'] = True  # Enable testing mode
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # In-memory SQLite DB

    with app.app_context():
        db.create_all()  # Create tables for the test
        for customer_data in TEST_CUSTOMERS:
            customer = CustomerDB(**customer_data)
            db.session.add(customer)
        db.session.commit()

    yield app

    with app.app_context():
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()


def test_get_customers(client):
    response = client.get('/api/v1/customers/')
    assert response.status_code == 200
    data = response.get_json()

    # Check structure of the response data
    assert 'customers' in data
    assert isinstance(data['customers'], list)
    assert len(data['customers']) == 2  # We added 2 test customers

    # Optionally check specific customer details
    expected_first_customer = TEST_CUSTOMERS[0]
    first_customer = data['customers'][0]

    assert first_customer['email'] == expected_first_customer['email']
    assert first_customer['name'] == expected_first_customer['name']
    # ... check other fields as needed