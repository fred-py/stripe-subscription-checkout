"""A difference when writing error handlers inside a
blueprint is that if the errorhandler decorator is used,
the handler will be invoked only for errors that originate in
the routes defined by the blueprint.
To install application-wide error handlers,
the app_errorhandler decorator must be used instead."""

# NOTE: Great resource: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xxiii-application-programming-interfaces-apis
from flask import render_template, request
from app import db
from app.errors import bp
from app.api.errors import error_response as api_error_response

# NOTE: error_response renamed as api_error_response for clarity


def wants_json_response():
    """Helper function, compares preference for
    JSON or HTML selected by the client in their
    list of preferred formats.
    If JSON rates higher, the function returns 
    a JSON response."""
    return request.accept_mimetypes['application/json'] >= \
        request.accept_mimetypes['text/html']


@bp.app_errorhandler(404)
def not_found_error(error):
    if wants_json_response():
        return api_error_response(404)
    return render_template('errors/404.html'), 404


@bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    if wants_json_response():
        return api_error_response(500)
    return render_template('errors/500.html'), 500