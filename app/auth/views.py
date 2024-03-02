from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, \
    current_user
from . import auth
from .. import db
from app.models import User
from app.emails import send_email
from .forms import LoginForm, RegistrationForm


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """Review page 133 and document this view function"""
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('db_views.index')
            return redirect(next)
        flash('Invalid email or password.')
    return render_template('/database/auth/login.html', form=form)


@auth.route('/logout')
@login_required  # Protect routes requiring the user to be logged in p.132
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('db_views.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data.lower(),
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You can now login.')
        return redirect(url_for('auth.login'))
    return render_template('database/auth/register.html', form=form)
