from flask import jsonify, request, g, url_for, current_app
from app.extensions import db
from ..models import CustomerDB, User, Permission
from . import api
from .decorators import permission_required
from .errors import forbidden


@api.route('/orders/')
def get_order_stats(id, last_seen):
    # Retunrs the total number of active orders in the database
    total_orders = CustomerDB.query.filter_by(active=True).count()

    new_orders = User.query.filter_by(id=id).count()

    return jsonify({'total_orders': total_orders, 'new_orders': new_orders})