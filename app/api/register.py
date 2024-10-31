import sqlalchemy as sa
from flask import jsonify, request, url_for, current_app
from app.extensions import db
from app.api import api
from app.api.auth import auth
from app.api.errors import bad_request
from app.models import User, Role
from app.emails import send_email


@api.route('/register', methods=['POST'])
def create_new_user():
    """Access User representation in JSON body of request.
    Returns dictionary representation of User object.
    415 error if client sends non-JSON format.
    400 error if JSON content is malformed.
    Both errors handles by handle_http_exception"""
    data = request.get_json()
    if 'username' not in data or 'email' not in data or 'password' not in data:
        return bad_request('Must include username, email and password fields')
    if db.session.scalar(sa.select(User).where(
            User.username == data['username'])):
        return bad_request('Username already in use')
    if db.session.scalar(sa.select(User).where(
            User.email == data['email'])):
        return bad_request('Email already in use')
    # NOTE: The constructor in User model was not able to access self.mail
    # when checking to set the self.role
    # Hence email must be passed as argument
    u = User(email=data['email'])
    u.from_dict(data, new_user=True)
    db.session.add(u)
    db.session.commit()
    return jsonify({
            'message': 'Registration successful. A confirmation email has been sent to your inbox.',
            'status': 'success'})



@api.route('/confirm/<token>')
@auth.login_required  # Protects route with custom decorator in api/auth.py
def confirm(token):
    # current_user is assigned as: auth.current_user() refer to api/auth.py
    user = auth.current_user()
    if user.confirmed:  # .confirmed is a bool column under User model default to false
        return jsonify(['user', 'authorised'])  # Redirect to home in vue app
    # Token confirmation is done  by the User model by calling confirm method
    if user.confirm(token):
        db.session.commit()
        # Send email to admin when a new user confirms their account
        send_email(current_app.config['UNITED_ADMIN'], 'New User',
                   'database/auth/email/new_user', user=auth.current_user)
    else:
        return jsonify('message', 'The confirmation link is invalid or has expired.')
    return jsonify('message', 'Token confirmation successful')








##NOTE *** The below is from AUTH - not part of API for reference only***

"""

@auth.route('/confirm/<token>')
@login_required  # Protect route with the @login_required decorator
def confirm(token):  # Users will be required to lon in before reaching this view function
    if auth.current_user.confirmed:  # If user is already confirmed, redirect to main page
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

"""