from app.extensions import db
from app.api import api
from app.api.auth import auth



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