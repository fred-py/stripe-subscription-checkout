from flask import jsonify, request, g, url_for, current_app
from flask_login import login_required, current_user
from app.extensions import db, cross_origin
from ..models import CustomerDB, User, Permission
from . import api
from .authentication import before_request
from .decorators import permission_required
from .errors import forbidden



@api.before_request  # requires auth
@api.route('/customers/')
@permission_required(Permission.DRIVER)
@cross_origin()
def get_customers():
    customers = CustomerDB.query.all()
    return jsonify({
        'customers': [
            customer.to_json() for customer in customers
        ]
    })


@api.route('/customers/<int:id>')
@permission_required(Permission.DRIVER)
@cross_origin()
def get_customer(id):
    """Returns a single customer.
    If name it not found in the database,
    a 404 error is returned."""
    customer = CustomerDB.query.get_or_404(id)
    return jsonify(customer.to_json())


@api.route('/customers/<int:id>', methods=['POST'])
@permission_required(Permission.ADMIN)
def edit_customer(id):
    """Edits a customer in the database.
    If the customer is not found, a 404 error
    is returned."""
    customer = CustomerDB.query.get_or_404(id)
    if g.current_user != g.current_user.can(Permission.ADMIN):
        return forbidden('Insufficient permissions')
    customer.name = request.json.get('name', customer.name)
    db.session.add(customer)
    db.session.commit()
    return jsonify(customer.to_json())
