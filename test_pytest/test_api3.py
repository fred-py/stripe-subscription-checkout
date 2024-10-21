import pytest
from flask import jsonify
from app.models import CustomerDB
from app.extensions import db
from app import create_app  # Assuming you have a factory function to create your Flask app

# Fixture to create a temporary, in-memory SQLite database for testing
@pytest.fixture(scope='module')
def test_client():
    app = create_app('testing')  
    #app.config['TESTING'] = True  # Enable testing mode
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # In-memory database

    with app.app_context():
        db.create_all()  # Create tables

    with app.test_client() as client:
        yield client

    with app.app_context():
        db.session.remove()
        db.drop_all()


# Test to verify the get_customers endpoint
def test_get_customers(test_client):
    # Sample customer data for testing
    customers = [
        CustomerDB(name="Test User", phone="1234567890", email="test@example.com", cus_id="cus_123", paymentintent_id="pi_123"),
        CustomerDB(name="Another User", phone="9876543210", email="another@example.com", cus_id="cus_456", paymentintent_id="pi_456")
    ]
    with test_client.application.app_context():
        db.session.add_all(customers)
        db.session.commit()

    response = test_client.get('/api/v1/customers/')
    assert response.status_code == 200
    data = response.get_json()

    # Compare the returned customer data with the expected data
    assert len(data['customers']) == 2
    assert data['customers'][0]['name'] == 'Test User'  # Assuming 'to_json' returns these fields

    assert any(item['email'] == 'test@example.com' for item in data['customers']) == True
    assert any(item['email'] == 'another@example.com' for item in data['customers']) == True