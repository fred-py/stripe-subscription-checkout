from app.extensions import db
from app.api import api
from app.api.auth import auth


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