from werkzeug.http import HTTP_STATUS_CODES
from werkzeug.exceptions import HTTPException
from app.api import api


# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xxiii-application-programming-interfaces-apis
def error_response(status_code, message=None):
    """Helper function to generate error response"""
    payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
    if message:
        payload['message'] = message
    return payload, status_code


def bad_request(message):
    """Handles requests with invalid
    data in the header"""
    return error_response(400, message)


@api.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of Flask's
    default HTML for HTTP errors."""
    return error_response(e.code)
