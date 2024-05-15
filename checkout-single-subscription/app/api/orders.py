from flask import jsonify, request, g, url_for, current_app
from app.extensions import db, cross_origin
from ..models import CustomerDB, User, Permission
from . import api
from .decorators import permission_required
from .errors import forbidden


@api.route('/orders/')
@cross_origin()
def get_order_stats():
    # Retunrs the total number of active orders in the database
    total_orders = CustomerDB.query.filter_by(active=True).count()

    """Add new orders logic here. use last_seen
    from User model"""

    return jsonify({'total_orders': total_orders})