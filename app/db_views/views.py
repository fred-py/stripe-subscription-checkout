
import os
from flask import render_template, redirect, url_for, abort, \
    flash, request, current_app, make_response, send_from_directory, jsonify

#from flask_login import login_required, current_user
#from flask_sqlalchemy import get_debug_queries
from . import db_views

from dotenv import load_dotenv, find_dotenv
#from ..db_operations.servicem8_operations.data_transfer import data_transfer as d
from ..db_operations.prepare_data import prepare_session_data, Customer
from ..db_operations.crud_operations import add_user
from ..db_operations.query_ops import CustomerQuery as cq  # get_cus_id, get_order_date, get_payment_intent 


load_dotenv(find_dotenv())


#port = int(os.environ.get('PORT', 4242))  # This is needed to deploy on fl0

@db_views.route('/database')  # Flask WebDev p. 140
def index():
    return render_template('/database/index.html')

@db_views.route('/user/<name>')
def user(name):
    return render_template('/database/user/user.html', name=name)

@db_views.route('/signup')
def signup():
    #return render_template('/database/auth/signup.html')
    pass