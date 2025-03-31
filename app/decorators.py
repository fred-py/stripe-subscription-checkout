"""Decorators below are used to make certain views accessible
only to users with the appropriate permissions."""

from functools import wraps
from flask import abort, Response, request
from flask_login import current_user
from .models import Permission
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


def permission_required(permission):
    """This decorator checks if the user has the required
    permissions to access the view. If the user does not have
    the required permissions, a 403 error is returned."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def admin_required(f):
    return permission_required(Permission.ADMIN)(f)




def basic_auth_required(f):
    """Temporary Basic Auth for API routes."""
    # Temporary Basic Auth decorator (no database)
    user = os.getenv('TEMP_USERNAME')
    word = os.getenv('TEMP_PASSWORD')
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or auth.username != user or auth.password != word:
            return Response(
                "Unauthorized Access", 401,
                {"WWW-Authenticate": 'Basic realm="Login Required"'}
            )
        return f(*args, **kwargs)
    return decorated


"""As a rule of thumb, the route decorator from
Flask should be given first when using multiple
decorators in a view function. The remaining decorators
should be given in the order in which they need to
evaluate when the view function is invoked.
In these two cases, the user authenticated state needs to
be checked first, since the user needs to be redirected to
the login prompt if found to not be authenticated.

Permissions may also need to be checked from templates, so
the Permission class with all its constants needs to be
accessible to them. 

To avoid having to add a template argument in every
render_template() call, a context processor can be used.
Context processors make variables available to all templates
during rendering. This change is shown in Example 9-8.""" # Page 340
