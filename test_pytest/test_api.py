import pytest
from flask import jsonify
from app import db, create_app
from app.models import CustomerDB
from datetime import datetime, timezone



# Create a fixture to create and destroy an in-memory SQLite database for each test
@pytest.fixture
def client():
    app = create_app('testing')
    with app.test_client() as client:
        with app.app_context():
            # Create the database tables
            db.create_all()
            yield client
            # Destroy the database tables after the test
            db.drop_all()


# Test data
customers_data = [
    {
        'id': 1,
        'name': 'John Doe',
        'email': 'john@example.com',
        'phone': '040478867',
        'cus_id': 'CUST001',
        'paymentintent_id': 'PAY001',
        'active': True,
        'test': False,
        'in_serviceM8': False,
        'cus_serviceM8_id': 'SERV001',
        'order_date': datetime.now(timezone.utc),
        'addresses': None,
        'bins': None,
        'subscriptions': None,
        'invoices': None
    },
    {
        'id': 2,
        'name': 'Jane Doe',
        'email': 'jane@example.com',
        'phone': '040422334',
        'cus_id': 'CUST002',
        'paymentintent_id': 'PAY002',
        'active': True,
        'test': False,
        'in_serviceM8': False,
        'cus_serviceM8_id': 'SERV002',
        'order_date': datetime.now(timezone.utc),
        'addresses': None,
        'bins': None,
        'subscriptions': None,
        'invoices': None
    }
]

# Mock the to_json method of the CustomerDB model
def mock_to_json(self):
    return {
            # CustomerDB columns
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'email': self.email,
            'cus_id': self.cus_id,
            'paymentintent_id': self.paymentintent_id,
            'active': self.active,
            'test': self.test,
            'order_date': self.order_date,
            # Address
            # Address contains the full address
            'addresss': self.addresses,
            'bins': self.bins,
            'subscriptions': self.subscriptions,
            'invoices': self.invoices
        }

# Test the get_customers endpoint
def test_get_customers(client, monkeypatch):
    # Add test data to the database
    for customer in customers_data:
        new_customer = CustomerDB(**customer)
        db.session.add(new_customer)
    db.session.commit()

    # Mock the to_json method
    monkeypatch.setattr(CustomerDB, 'to_json', mock_to_json)

    # Make a GET request to the /customers/ endpoint
    response = client.get('/api/v1/customers/')


    # Assert that the response status code is 200
    assert response.status_code == 200

    # Assert that the response content type is application/json
    assert response.content_type == 'application/json'

    # Assert that the response data matches the expected data
    expected_response = jsonify({'customers': customers_data})
    assert response.json == expected_response.json