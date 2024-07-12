from app.extensions import db
from app.api import api
from app.api.auth import auth
from app.api.auth import token_auth


# NOTE: Test on terminal by running
# $ http --auth '<email>':'<password>' POST http://localhost:5000/api/v1/tokens

# decorator auth.login_required is
# from HTTPBasicAuth instance
# Instructs Flask-HTTPAuth to
# verify authentication function
# in app/api/auth.py
@api.route('/tokens', methods=['POST'])
@auth.login_required
def get_token():
    """Returns token for authenticated user
    NOTE: current_user is assigned as
    auth.current_user
    this refers to 'auth = HTTPBasicAuth'
    variable assigned in app/api/auth.py"""
    token = auth.current_user().get_token()
    db.session.commit()
    return {'token': token}


@api.route('/tokens', methods=['DELETE'])
@token_auth.login_required
def revoke_token():
    """This route allows clients to invalidate
    their authentication token by sending a
    DELETE request to the /tokens URL.
    The token to be invalidated is provided
    in the Authorization header of the request.
    The token's expiration date is reset
    using a helper method in the User class,
    effectively revoking it. Changes are
    committed to the database to ensure the
    token is invalidated.
    The route responds with a 204 status code,
    indicating success with no content
    to return.
    Test with HTTPie:
    $ http -A bearer --auth <token> DELETE
    http://localhost:5000/api/v1/tokens"""
    token_auth.current_user().revoke_token()
    db.session.commit()
    return '', 204
