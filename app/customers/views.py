from flask import render_template, redirect, request, \
    url_for, flash, current_app
from flask_login import login_user, logout_user, \
    login_required, current_user
from .. import db
from app.models import User, CustomerDB
from app.emails import send_email

from . import customers

@login_required
@customers.route('/customers', methods=['GET', 'POST'])
def customers_info():
    customers = CustomerDB.query.all()
    return render_template('database/customers/customers.html', customers=customers)
