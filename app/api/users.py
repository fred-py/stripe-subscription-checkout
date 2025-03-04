import sqlalchemy as sa
from flask import jsonify, url_for, request, current_app
from app.api import api
from app.api.errors import bad_request
from ..models import User, CustomerDB, Lead, Address, Bin
from app.extensions import db
from app.api.auth import token_auth, auth
from app.decorators import permission_required, admin_required
from app.emails import send_email

# NOTE: Great resource: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xxiii-application-programming-interfaces-apis

# Protect API Routes with tokens
# Using @token_auth.login_required
# NOTE: Requests sent to any routes with the 
# @token_auth decorator, will have to add the
# Authorisation header, with the token received
# from the /tokens endpoint.
# Flask-HTTPAuth expects the token to be
# sent as a "bearer" token, which can be
# sent with HTTPie as follows:
# (venv) $ http -A bearer --auth <token> GET http://localhost:5000/api/users/1

@api.route('users/<int:id>', methods=['GET'])
@token_auth.login_required
def get_user(id):
    """Retrieves single user by id
    returns 404 if None"""
    return db.get_or_404(User, id).to_dict()


@api.route('/users/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_user(id):
    """ Loads & updates user information
    Returns 404 if user is not found
    Use in terminal:

    $ http PUT http://localhost:5000/api/v1/users/2
    "email=enter@differentemail.com"

    Same method can be applied for other fields
    in the User model.
    NOTE: More logic is needed to
    update User permissions"""
    user = db.get_or_404(User, id)
    data = request.get_json()
    if 'username' in data and data['username'] != user.username and \
        db.session.scalar(sa.select(User).where(
            User.username == data['username'])):
        return bad_request('please use a different username')
    if 'email' in data and data['email'] != user.email and \
        db.session.scalar(sa.select(User).where(
            User.email == data['email'])):
        return bad_request('please use a different email address')
    user.from_dict(data, new_user=False)
    db.session.commit()
    return user.to_dict()


@api.route('/customers/')
#@admin_required  # NOTE; when running is_administrator() on adm user still returns false Look into it Chap.9
@token_auth.login_required
def get_customers():
    """Test with HTTPie:
    $ http -A bearer --auth "<token>" GET
    http://localhost:5000/api/v1/customers/"""
    customers = CustomerDB.query.all()
    return jsonify({
       'customers': [
           customer.to_json() for customer in customers
        ]
    })


@api.route('/customers/<int:id>')
#@permission_required(Permission.DRIVER)
#@cross_origin()
#@token_auth.login_required
def get_customer(id):
    """Returns a single customer.
    If name it not found in the database,
    a 404 error is returned."""
    customer = CustomerDB.query.get_or_404(id)
    return jsonify(customer.to_json())


@api.route('/leads/')
#@admin_required  # NOTE; when running is_administrator() on adm user still returns false Look into it Chap.9
@token_auth.login_required
def get_leads():
    """Test with HTTPie:
    $ http -A bearer --auth "<token>" GET
    http://localhost:5000/api/v1/leads/"""
    leads = Lead.query.all()
    return jsonify({
        'leads': [
            lead.to_json() for lead in leads
        ]
    })

@api.route('/leads/<int:id>')
def get_lead(id):
    """Returns a single lead.
    If name it not found in the database,
    a 404 error is returned."""
    lead = Lead.query.get_or_404(id)
    return jsonify(lead.to_json())


@api.route('/edit-customer/<int:id>/', methods=['GET', 'PUT'])
#@token_auth.login_required
def edit_customer(id):
    """Test w/o auth
    http PUT  http://localhost:5000/api/v1/customers/<int:id>/ email=newemail@here.com

    Args:
        <int:id>: id linked to customer details being edited

    NOTE: cus id is passed as id=<int> and new name as name=<str>"""

    customer = CustomerDB.query.get(id)
    if not customer:
        return jsonify({'message': 'Customer not found'}), 404

    data = request.get_json()
    if 'name' in data and data['name'] != customer.name:
        customer.name = data['name']
    if 'email' in data and data['email'] != customer.email:
        customer.email = data['email']
    if 'phone' in data and data['phone'] != customer.phone:
        customer.phone = data['phone']
    if 'street' in data and data['street'] != customer.addresses.street:
        customer.addresses.street = data['street']
    if 'city' in data and data['city'] != customer.addresses.city:
        customer.addresses.city = data['city']
    if 'postcode' in data and data['postcode'] != customer.addresses.postcode:
        customer.addresses.postcode = data['postcode'] 
    if 'bin_collection' in data and data['bin_collection'] != customer.bins.bin_collection:
        customer.bins.bin_collection = data['bin_collection']
    if 'selected_bins' in data and data['selected_bins'] != customer.bins.selected_bins:
        customer.bins.selected_bins = data['selected_bins']
    if 'clean_date' in data and data['clean_date'] != customer.bins.clean_date:
        customer.bins.clean_date = data['clean_date']

    db.session.commit()

    return jsonify(customer.to_json())