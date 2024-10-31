# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xxiii-application-programming-interfaces-apis
from flask import Blueprint

api = Blueprint('api', __name__)

from app.api import errors, users, tokens, register