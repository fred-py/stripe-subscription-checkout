from flask import render_template, redirect, request, \
    url_for, flash, current_app, abort
from flask_login import login_user, logout_user, \
    login_required, current_user
from .. import db
from app.models import User, CustomerDB
from app.emails import send_email

from . import customers




@customers.route('/customers_test', methods=['GET', 'POST'])
@login_required  # NOTE: First route attempeting to display all customers
def customers_info():
    customers = CustomerDB.query.all()
    return render_template(
        'database/customers/customers.html', customers=customers
    )



@customers.route('/customers')
@login_required
def index():
    return render_template('database/customers/editable_table.html')


@login_required
@customers.route('/search')
def search_data():
    query = CustomerDB.query
    # search filter
    search = request.args.get('search')
    if search:
        query = query.filter(db.or_(
            CustomerDB.name.like(f'%{search}%'),
            CustomerDB.email.like(f'%{search}%'),
            CustomerDB.phone.like(f'%{search}%'),
        ))
    total = query.count()

    # sorting
    sort = request.args.get('sort')
    if sort:
        order = []
        for s in sort.split(','):
            direction = s[0]
            name = s[1:]
            if name not in ['name', 'email']:
                name = 'name'
            col = getattr(CustomerDB, name)
            if direction == '-':
                col = col.desc()
            order.append(col)
        if order:
            query = query.order_by(*order)

    # pagination
    start = request.args.get('start', type=int, default=-1)
    length = request.args.get('length', type=int, default=-1)
    if start != -1 and length != -1:
        query = query.offset(start).limit(length)

    #cus = {'data': [customer.to_dict() for customer in query]}
    #print(cus)

    # response
    return {
        'data': [customer.to_dict() for customer in query],
        'total': total,
    }



@login_required
@customers.route('/update', methods=['POST'])
def update():
    data = request.get_json()
    if 'id' not in data:
        abort(400)
    customer = CustomerDB.query.get(data['id'])
    for field in ['name', 'address', 'phone', 'email', 'bin_collection', 'clean_date']:
        if field in data:
            setattr(customer, field, data[field])
    db.session.commit()
    return '', 204
