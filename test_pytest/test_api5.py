import pytest
from flask import jsonify

from app.extensions import db
from app.models import CustomerDB
from app import create_app

class TestApi:

    TEST_CUSTOMERS = [
        {'name': 'Active John', 'phone': '555-1234', 'email': 'activejohn@example.com', 'cus_id': 'cus_123', 'paymentintent_id': 'pi_123', 'active': True},
        {'name': 'Inactive Jane', 'phone': '555-5678', 'email': 'inactivejane@example.com', 'cus_id': 'cus_456', 'paymentintent_id': 'pi_456', 'active': False}
    ]

    @pytest.fixture
    def app(self):
        app = create_app('testing')

        with app.app_context():
            db.create_all()
            for customer_data in self.TEST_CUSTOMERS:
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

        # Example check for active customer
        active_customers = [c for c in data['customers'] if c['active']]
        assert len(active_customers) == 1

    def test_get_order_stats(self, client):
        response = client.get('/api/v1/orders/')
        assert response.status_code == 200
        data = response.get_json()
        
        assert 'total_orders' in data
        assert data['total_orders'] == 1  # We have 1 active order in test data