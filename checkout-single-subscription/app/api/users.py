import sqlalchemy as sa
from flask import jsonify, url_for, request
from app.api import api
from app.api.errors import bad_request
from ..models import User, CustomerDB
from app.extensions import db

# NOTE: Great resource: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xxiii-application-programming-interfaces-apis


@api.route('users/<int:id>', methods=['GET'])
def get_user(id):
    """Retrieves single user by id
    returns 404 if None"""
    return db.get_or_404(User, id).to_dict()

@api.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    """
    Updates user information
    Use in terminal:

    $ http PUT http://localhost:5000/api/v1/users/2
    "email=enter@differentemail.com"

    Same method can be applied for other fields
    in the User model.
    """
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

@api.route('/register/', methods=['POST'])
def create_user():
    """
    Access User representation in JSON body of request.
    Returns dictionary representation of User object.
    415 error if client sends non-JSON format.
    400 error if JSON content is malformed.
    Both errors handles by handle_http_exception
    """
    data = request.get_json()
    # Check the 3 mandatory fields
    if 'username' not in data or 'email' not in data or 'password' not in data:
        return bad_request('must include username, email, and password fields')
    if db.session.scalar(sa.select(User).where(
            User.username == data['username'])):
        return bad_request('please use a different username')
    if db.session.scalar(sa.select(User).where(
            User.email == data['email'])):
        return bad_request('please use a different email address')
    user = User()
    user.from_dict(data, new_user=True)
    db.session.add(user)
    db.session.commit()
    # 201 is the status code for a successfull POST request
    # HTTP protocol requires that the response includes a Location header
    # This is set in to the URL of the new resource using url_for()
    return user.to_dict(), 201, {'Location': url_for('api.get_user', id=user.id)}

@api.route('/customers/')
def get_customers():
    customers = CustomerDB.query.all()
    return jsonify({
       'customers': [
           customer.to_json() for customer in customers
        ]
    })

@api.route('/customers/<int:id>')
#@permission_required(Permission.DRIVER)
#@cross_origin()
def get_customer(id):
    """Returns a single customer.
    If name it not found in the database,
    a 404 error is returned."""
    customer = CustomerDB.query.get_or_404(id)
    return jsonify(customer.to_json())
