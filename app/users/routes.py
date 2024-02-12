
from flask import render_template
from app.users import bp

@bp.route('/')  # This is similar to app.route('/')
def index():
    return render_template('users/index.html')

@bp.route('/users/', methods=['GET', 'POST'])  # This is similar to app.route('/models/', methods=['GET', 'PO
def users():
    return render_template('users/users.html')