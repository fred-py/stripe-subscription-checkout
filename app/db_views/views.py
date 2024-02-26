
import os
from flask import render_template, redirect, session, url_for, abort, \
    flash, request, current_app, make_response, send_from_directory, jsonify
#from flask_login import login_required, current_user
#from flask_sqlalchemy import get_debug_queries
from . import db_views
from datetime import datetime
from dotenv import load_dotenv, find_dotenv
from .forms import RegisterAcc
from app.models import User, Role, CustomerDB, \
    Address, Subscription, Bin, Invoice
from app.extensions import db

#from ..db_operations.servicem8_operations.data_transfer import data_transfer as d
#from ..db_operations.prepare_data import prepare_session_data, Customer
#from ..db_operations.crud_operations import add_user
#from ..db_operations.query_ops import CustomerQuery as cq  # get_cus_id, get_order_date, get_payment_intent 

load_dotenv(find_dotenv())

#port = int(os.environ.get('PORT', 4242))  # This is needed to deploy on fl0

with current_app.app_context():
    @current_app.shell_context_processor
    def make_shell_context():
        """This function is used to add the
        database instance and models to the shell context"""
        return dict(db=db, User=User, Role=Role)

@db_views.route('/database', methods=['GET', 'POST'])  # Flask WebDev p. 140
def index():
    # Access congig variables using current_app.config
    secret_key = current_app.config['SECRET_KEY']
    form = RegisterAcc()
    # validate_on_submit() invokes the DataRequired() validator
    # If it returns True
    # the session name is assigned to the local var name
    if form.validate_on_submit():  # Flask WebDev p. 118
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        return redirect(url_for('db_views.index'))
        # The form field is cleared by setting it to an empty string
        # This is done so the form is blank when the form is rendered again
        #form.name.data = ''
    return render_template(
        '/database/index.html',
        form=form, name=session.get('name'),
        known=session.get('known', False),
        current_time=datetime.utcnow()
    )


@db_views.route('/user/<name>')
def user(name):
    return render_template('/database/user/user.html', name=name)

@db_views.route('/signup')
def signup():
    #return render_template('/database/auth/signup.html')
    pass

