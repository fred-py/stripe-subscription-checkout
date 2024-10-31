from flask import current_app, jsonify
import sqlalchemy as sa
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from app.extensions import db
from ..models import User
from app.api.errors import error_response

# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xxiii-application-programming-interfaces-apis
# Basic authentication flow from flask_httpauth
# NOTE: current_user is assigned as:
# auth.current_user()
auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()  # Provides token verification callback


@auth.verify_password
def verify_password(email, password):
    """Receives username and password
    from the client and returns the
    authenticated user if credentials
    are valid.
    The authenticated user will be
    available as auth.current_user(),
    so that it can be used in the API
    view functions."""
    user = db.session.scalar(sa.select(User).where(
        User.email == email))
    if user and user.verify_password(password):
        return user


@auth.error_handler
def basic_auth_error(status):
    """status argument is the HTTP
    status code. Returns 401 if authentication
    is invalid 'Unauthorized' error."""
    return error_response(status)


@token_auth.verify_token
def verify_token(token):
    """When using token authentication, Flask-HTTPAuth
    uses a verify_token decorated function.
    Other than that, token authentication works
    in the same way as basic authentication.
    Token verification function uses
    User.check_token() to locate the
    user that owns the provided token
    and return it. None return causes the
    client to be rejected with an authentication
    error"""
    return User.check_token(token) if token else None



@token_auth.error_handler
def token_auth_error(status):
    return error_response(status)