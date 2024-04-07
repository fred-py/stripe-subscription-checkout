"""Flask handles error 404 & 500 by default,
returning a HTML response. This can confuse the
API client if it expects a JSON response.

This error handler adapts the response based
on the format requested by the client."""

from flask import render_template, request, jsonify
from app.exceptions import ValidationError
from . import db_views, api


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


def forbidden(message):
    """Custom error handler for 403 Forbidden errors"""
    response = jsonify({'error': 'forbidden', 'message': message})
    response.status_code = 403
    return response


def bad_request(message):
    response = jsonify({'error': 'bad request', 'message': message})
    response.status_code = 400
    return response


def unauthorized(message):
    response = jsonify({'error': 'unauthorized', 'message': message})
    response.status_code = 401
    return response


@api.errorhandler(ValidationError)
def validation_error(e):  # p.455
    return bad_request(e.args[0])