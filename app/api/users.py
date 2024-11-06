import sqlalchemy as sa
from flask import jsonify, url_for, request, current_app
from app.api import api
from app.api.errors import bad_request
from ..models import User, CustomerDB, Address
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


@api.route('/customers/<int:id>/name', methods=['PUT'])
#@token_auth.login_required
def update_customer_name(id):
    """Test w/o auth
    http PUT  http://localhost:5000/api/v1/c
    ustomers/1/name id=1 name=Josephina
    NOTE: cus id is passed as id=<int> and new name as name=<str>"""
    customer = CustomerDB.query.get_or_404(id)
    data = request.get_json()
    if 'name' in data:
        customer.name = data['name']
        db.session.commit()
        return jsonify(customer.to_json()), 200
    return jsonify({'error': 'Invalid data'}), 400


@api.route('/customers/<int:customer_id>/email', methods=['PUT'])
#@token_auth.login_required
def update_customer_email(customer_id):
    """Test w/o auth
    http PUT  http://localhost:5000/api/v1/customers/1/email id=1 email=<str>"""
    customer = CustomerDB.query.get_or_404(customer_id)
    data = request.get_json()
    if 'email' in data:
        customer.email = data['email']
        db.session.commit()
        return jsonify(customer.to_json()), 200
    return jsonify({'error': 'Invalid data'}), 400


@api.route('/customers/<int:customer_id>/phone', methods=['PUT'])
#@token_auth.login_required
def update_customer_phone(customer_id):
    customer = CustomerDB.query.get_or_404(customer_id)
    data = request.get_json()
    if 'phone' in data:
        customer.phone = data['phone']
        db.session.commit()
        return jsonify(customer.to_json()), 200
    return jsonify({'error': 'Invalid data'}), 400


@api.route('/customers/<int:customer_id>/address', methods=['PUT'])
#@token_auth.login_required
def update_customer_address(customer_id):
    customer = CustomerDB.query.get_or_404(customer_id)
    data = request.get_json()
    if 'street' in data and 'city' in data and 'state' in data and 'postcode' in data:
        address = Address(
            street=data['street'],
            city=data['city'],
            state=data['state'],
            postcode=data['postcode'],
            customer_id=customer_id
        )
        customer.addresses = address
        db.session.commit()
        return jsonify(customer.to_json()), 200
    return jsonify({'error': 'Invalid data'}), 400


@api.route('/customers_test/<int:id>/', methods=['GET', 'PUT'])
def edit_customer_test(id):
    customer = CustomerDB.query.get(id)
    if not customer:
        return jsonify({'message': 'Customer not found'}), 404

    data = request.get_json()
    if 'name' in data:
        customer.name = data['name']
    if 'email' in data:
        customer.email = data['email']
    if 'phone' in data:
        customer.phone = data['phone']
    if 'addresses' in data:
        if customer.addresses:
            customer.addresses.street = data['addresses'].get('street', customer.addresses.street)
            customer.addresses.city = data['addresses'].get('city', customer.addresses.city)
            customer.addresses.state = data['addresses'].get('state', customer.addresses.state)
            customer.addresses.postcode = data['addresses'].get('postcode', customer.addresses.postcode)
        else:
            new_address = Address(**data['addresses'])
            customer.addresses = new_address
        db.session.commit()

    return jsonify(customer.to_json())