import json
import pytest
from app import db, create_app
from app.models import CustomerDB
from datetime import datetime, timezone

# Mock data
@pytest.fixture
def mock_customers():
    return [
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

# Mock the database query
@pytest.fixture
def mock_query(mocker, mock_customers):
    mock = mocker.patch('your_app.CustomerDB.query')
    mock.all.return_value = [CustomerDB(**customer) for customer in mock_customers]
    return mock

# Test the endpoint
def test_get_customers(mock_query, mock_customers):
    with db.test_client() as client:
        response = client.get('/customers/')
        assert response.status_code == 200
        assert response.json == {'customers': mock_customers}