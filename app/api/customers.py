from flask import jsonify, request, g, url_for, current_app
from .. import db
from ..models import CustomerDB, Permission
from . import api
from .decorators import permission_required
from .errors import forbidden


@api.route('/customers/')
def get_customers():
    customers = CustomerDB.query.all()
    return jsonify({
        'customers': [
            customer.to_json() for customer in customers
        ]
    })


@api.route('/customers/<str:name>')
def get_customer(name):
    """Returns a single customer.
    If name it not fouind in the database,
    a 404 error is returned."""
    customer = CustomerDB.query.get_or_404(name)
    return jsonify(customer.to_json())


@api.route('/customers/<str:name>', methods=['POST'])
@permission_required(Permission.WRITE)
def edit_customer(name):
    """Edits a customer in the database.
    If the customer is not found, a 404 error
    is returned."""
    customer = CustomerDB.query.get_or_404(name)
    if g.current_user != g.current_user.can(Permission.ADMIN):
        return forbidden('Insufficient permissions')
    customer.name = request.json.get('name', customer.name)
    db.session.add(customer)
    db.session.commit()
    return jsonify(customer.to_json())
