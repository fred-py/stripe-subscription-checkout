import sqlalchemy as sa
from flask_httpauth import HTTPBasicAuth
from app.extensions import db
from ..models import User
from app.api.errors import error_response

# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xxiii-application-programming-interfaces-apis
# Basic authentication flow from flask_httpauth
# NOTE: current_user is assigned as:
# auth.current_user()
auth = HTTPBasicAuth()


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
