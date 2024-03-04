from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, \
    current_user
from . import auth
from .. import db
from app.models import User
from app.emails import send_email
from .forms import LoginForm, RegistrationForm


@auth.before_request  # Page. 286 before_request handler to intercept all blueprint requests
def before_request():     # @before_app_request can be used to intercept all requests to the application
    """This view allows unfinished users to confirm their
    email before accessing the application.
    This handler will intercept requests if all
    the following conditions are met:
    1. The user is logged in
    2. The user is not confirmed
    3. The request is not for the authentication blueprint
    4. The request is not for a static file"""
    if current_user.is_authenticated \
            and not current_user.confirmed \
            and request.blueprint != 'auth' \
            and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))

@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('db_views.index'))
    return render_template('database/auth/unconfirmed.html')

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
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm Your Account',
                   'database/auth/email/confirm', user=user, token=token)
        flash('A confirmation email has been sent to your inbox.\
              Please check spam folder if you do not see it in your inbox')
        return redirect(url_for('auth.login'))
    return render_template('database/auth/register.html', form=form)


@auth.route('/confirm/<token>')
@login_required  # Protect route with the @login_required decorator
def confirm(token):  # Users will be required to lon in before reaching this view function
    if current_user.confirmed:  # If user is already confirmed, redirect to main page
        return redirect(url_for('db_views.index'))  
    if current_user.confirm(token):  # Token confirmation is done entirely by the User model by calling confirm
        db.session.commit()
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('db_views.index'))


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account',
               'auth/email/confirm', user=current_user, token=token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('db_views.index'))
