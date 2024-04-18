from flask import render_template, redirect, request, \
    url_for, flash, current_app
from flask_login import login_user, logout_user, \
    login_required, current_user
from . import auth
from .. import db
from app.models import User
from app.emails import send_email
from .forms import LoginForm, RegistrationForm, \
    ChangePasswordForm, PasswordResetRequestForm, \
    PasswordResetForm, ChangeEmailForm


@auth.before_app_request  # Page. 286 before_request handler to intercept all blueprint requests
def before_request():     # @before_app_request can be used to intercept all requests to the application
    """This view allows unfinished users to confirm their
    email before accessing the application.
    This handler will intercept requests if all
    the following conditions are met:
    1. The user is logged in
    2. The user is not confirmed
    3. The request is not for the authentication blueprint
    4. The request is not for a static file"""
    if current_user.is_authenticated:
        current_user.ping()  # Update the last seen time for the user
        if not current_user.confirmed \
                and request.endpoint \
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
        # Send email to admin when a new user confirms their account
        send_email(current_app.config['UNITED_ADMIN'], 'New User',
                   'database/auth/email/new_user', user=current_user)
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('database.index'))


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account',
               'auth/email/confirm', user=current_user, token=token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('db_views.index'))


# Password Updates
@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash('Your password has been updated.')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid password.')
    return render_template("database/auth/change_password.html", form=form)


@auth.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for('db_views.index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user:
            token = user.generate_reset_token()
            send_email(user.email, 'Reset Your Password',
                       'database/auth/email/reset_password',
                       user=user, token=token,
                       next=request.args.get('next'))
        flash('An email with instructions to reset your password has been sent to you.')
        return redirect(url_for('auth.login'))
    return render_template('database/auth/reset_password.html', form=form)


@auth.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        if User.reset_password(token, form.password.data):
            db.session.commit()
            flash('Your password has been updated.')
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('db_views.index'))
    return render_template('database/auth/reset_password.html', form=form)


@auth.route('/change_email', methods=['GET', 'POST'])
@login_required
def change_email_request():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.email.data.lower()
            token = current_user.generate_email_change_token(new_email)
            send_email(new_email, 'Confirm your email address',
                       'database/auth/email/change_email',
                       user=current_user, token=token)
            flash('An email with instructions to confirm your new email '
                  'address has been sent to you.')
            return redirect(url_for('db_views.index'))
        else:
            flash('Invalid email or password.')
    return render_template("database/auth/change_email.html", form=form)


@auth.route('/change_email/<token>')
@login_required
def change_email(token):
    if current_user.change_email(token):
        db.session.commit()
        flash('Your email address has been updated.')
    else:
        flash('Invalid request.')
    return redirect(url_for('db_views.index'))