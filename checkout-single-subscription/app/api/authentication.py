from flask import g, jsonify, request, current_app, \
    redirect, flash, url_for, make_response
# This user auth will only be used in the API blueprint
# Hence the flask_httpauth is initialised in the blueprint
from flask_httpauth import HTTPBasicAuth
from flask_login import login_user, logout_user, \
    login_required, current_user
from flask_wtf.csrf import CSRFProtect
from app.emails import send_email
from ..auth.forms import LoginForm, RegistrationForm, \
    ChangePasswordForm, PasswordResetRequestForm, \
    PasswordResetForm, ChangeEmailForm
from ..models import User
from . import api
from .. import db
from .errors import unauthorized, forbidden  # Error handlers in API Directory not db_views

# NOTE: refer to link below for SPA + Flask Auth Implementation
# https://testdriven.io/blog/flask-spa-auth/#session-vs-token-based-auth
auth = HTTPBasicAuth()

# The Flask-HTTPAuth extension also invoke the callback
# for requests that carry no authentication information.
# Setting both arguments∫ to the empty string,
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
@api.before_request
@auth.login_required  # Auth check will be done automatically for all routes in the blueprint
def before_request():
    """The before_request handler is registered
    with the blueprint, ensuring that it runs before
    any request in the blueprint. This handler is
    responsible for verifying the authentication of
    the client. Must be included in all api routes
    that require auth"""
    if not g.current_user.is_anonymous and \
            not g.current_user.confirmed:
        return forbidden('Unconfirmed account')

#@api.after_request
#def set_xsrf_cookie(response):
#    """Set the XSRF cookie on the response"""
#    csrf_token = CSRFProtect.create_token()
#    response.set_cookie('XSRF-TOKEN', csrf_token)
#    return response

@api.route('/login', methods=['POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():     
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user and user.verify_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            # Return a JSON response with a success message and user data
            auth_token = user.generate_auth_token(expiration=3600)
            response = {
                'message': 'Login successful',
                'token': auth_token,
            }
            return make_response(jsonify(response)), 200
        else:
            # Return an error response if login fails
            response = {'message': 'Invalid email or password'}
            return make_response(jsonify(response)), 401

    # If the form is not validated, return a bad request response
    response = {'message': 'Invalid request data'}
    return make_response(jsonify(response)), 400


@api.route('/register', methods=['POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data.lower(),
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm Your Account',
                   'database/auth/email/confirm', user=user, token=token)
        flash('A confirmation email has been sent to your inbox.\
              Please check spam folder if you do not see it in your inbox')
        return redirect(url_for('api.login'))
    return redirect(url_for('api.register'))


@api.route('/logout', methods=['POST'])
def logout():
    logout_user()
    response = {'message': 'Logout successful'}
    return make_response(jsonify(response)), 200

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