#  “error handlers in main blueprint”
"""“A difference when writing error handlers inside a
blueprint is that if the errorhandler decorator is used,
the handler will be invoked only for errors that originate in
the routes defined by the blueprint.
To install application-wide error handlers,
the app_errorhandler decorator must be used instead.”

Page 119 of Flask Web Development, 2nd Edition"""

from flask import render_template, request, jsonify
from . import db_views


@db_views.app_errorhandler(403)
def forbidden(message):
    """Custom error handler for 403 Forbidden errors"""
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'forbidden', 'message': message})
        response.status_code = 403
        return response
    return render_template('/database/403.html'), 403


@db_views.app_errorhandler(404)
def page_not_found(e):
    """Checks the accept header of the request which
    is decoded into request.accept_mimetypes.
    JSON response is generated only for clients
    that include JSON in the list of accepted
    formats, but not HTML."""
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'not found'})
        response.status_code = 404
        return response
    return render_template('/database/404.html'), 404


@db_views.app_errorhandler(500)
def internal_server_error(e):
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'internal server error'})
        response.status_code = 500
        return response
    return render_template('/database/500.html'), 500

# The remaining status codes are generated explicitly by
# the web service, so they can be implemented as helper functions
# inside the blueprint in the errors.py module.
# View functions in the API blueprint can invoke
# these helper functions to generate error responses as needed.
