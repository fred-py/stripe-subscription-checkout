from flask import g, jsonify
# This user auth will only be used in the API blueprint
# Hence the flask_httpauth is initialised in the blueprint
from flask_httpauth import HTTPBasicAuth
from ..models import User
from . import api
from .errors import unauthorized, forbidden


auth = HTTPBasicAuth()

# The Flask-HTTPAuth extension also invoke the callback
# for requests that carry no authentication information.
# Setting both arguments to the empty string,
# in this case when the email is empty, the func returns false


@auth.verify_password
def verify_password(email, password):
    """Email l& password verification are carried
    out using the existing support in the User model.
    The verification callback returns True when the login
    is valid and False otherwise."""
    if email == '':
        return False
    user = User.query.filter_by(email=email).first()
    if not user:
        return False
    g.current_user = user
    return user.verify_password(password)


@auth.error_handler
def auth_error():
    """The error handler for authentication errors
    generates a 401 response with a JSON body."""
    return unauthorized('Invalid credentials')


@api.before_request
@auth.login_required  # Auth check will be done automatically for all routes in the blueprint
def before_request():
    """The before_request handler is registered
    with the blueprint, ensuring that it runs before
    any request in the blueprint. This handler is
    responsible for verifying the authentication of
    the client."""
    if not g.current_user.is_anonymous and \
            not g.current_user.confirmed:
        return forbidden('Unconfirmed account')