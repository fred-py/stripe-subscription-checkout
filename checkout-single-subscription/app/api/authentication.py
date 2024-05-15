from flask import g, jsonify
# This user auth will only be used in the API blueprint
# Hence the flask_httpauth is initialised in the blueprint
from flask_httpauth import HTTPBasicAuth
from ..models import User
from . import api
from .errors import unauthorized, forbidden  # Error handlers in API Directory not db_views


auth = HTTPBasicAuth()

# The Flask-HTTPAuth extension also invoke the callback
# for requests that carry no authentication information.
# Setting both arguments to the empty string,
# in this case when the email is empty, the func returns false


@auth.verify_password
def verify_password(email_or_token, password):  
    """Email_or_token & password verification are carried
    out using the existing support in the User model.
    If password is blank, email_or_token is assumed
    to be an API token and validated as such.
    If both fields are non-empty then regular
    email & password authentication is performed
    Token-based auth is optional(up to each client),
    g.token_used is added so the view function
    can distinguish between the two
    authentication methods."""
    # FlaskWebDevelopment, 2nd Edition, p. 461
    if email_or_token == '':
        return False
    if password == '':
        g.current_user = User.verify_auth_token(email_or_token)
        g.token_used = True
        return g.current_user is not None
    user = User.query.filter_by(email=email_or_token).first()
    if not user:
        return False
    g.current_user = user
    g.token_used = False
    return user.verify_password(password)


@auth.error_handler
def auth_error():
    """The error handler for authentication errors
    generates a 401 response with a JSON body."""
    return unauthorized('Invalid credentials')

"""Log in required is temporally disabled
Once enlable, log in form on vue app will
be needed to post token as per token route below"""
#@api.before_request
#@auth.login_required  # Auth check will be done automatically for all routes in the blueprint
def before_request():
    """The before_request handler is registered
    with the blueprint, ensuring that it runs before
    any request in the blueprint. This handler is
    responsible for verifying the authentication of
    the client."""
    if not g.current_user.is_anonymous and \
            not g.current_user.confirmed:
        return forbidden('Unconfirmed account')


@api.route('/tokens/', methods=['POST'])
def get_token():
    """Returns an authentication token to the client.
    Prevents clients from authenticating to this route
    using previously obtained token instead of an
    email address and password.
    g.token_used  var is checked and requests 
    authenticated with a token are rejected.
    This prevents users from bypassing the token
    expiration time by requesting a new token using
    the old token authentication.
    Flask WebDev p. 449"""
    if g.current_user.is_anonymous or g.token_used:
        return unauthorized('Invalid credentials')
    return jsonify({'token': g.current_user.generate_auth_token(
            expiration=3600), 'expiration': 3600})  # 1h validity period