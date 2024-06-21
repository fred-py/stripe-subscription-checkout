from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from flask import current_app, url_for, request
from flask_login import UserMixin, AnonymousUserMixin
#from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer

import jwt
from datetime import datetime, timedelta, timezone
from jwt import ExpiredSignatureError, InvalidTokenError

from itsdangerous import BadSignature, SignatureExpired
from app.exceptions import ValidationError
from .extensions import db, login_manager


# Create association table
# https://realpython.com/python-sqlite-sqlalchemy/#table-creates-associations
# Flask Web Development 2nd Edition, p. 90

class Permission:
    USER = 1
    DRIVER = 2
    ADMIN = 6

    def __repr__(self) -> str:
        return f'Only 2 types of permissions - \
            1. User: {self.USER}, 2. Admin: {self.ADMIN}'


# NOTE Migration needed after changes to the models
class CustomerDB(db.Model):
    __tablename__ = 'customers'
    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    name: Mapped[str] = db.Column(db.String, nullable=False)
    phone: Mapped[str] = db.Column(db.String, nullable=False)
    email: Mapped[str] = db.Column(db.String, nullable=False, unique=True)
    cus_id: Mapped[str] = db.Column(db.String, nullable=False)
    paymentintent_id: Mapped[str] = db.Column(db.String, nullable=False)
    active: Mapped[bool] = db.Column(db.Boolean, default=True)
    test: Mapped[bool] = db.Column(db.Boolean, default=False)
    in_serviceM8: Mapped[bool] = db.Column(db.Boolean, default=False)
    cus_serviceM8_id: Mapped[str] = db.Column(db.String, default=False)
    order_date: Mapped[datetime] = db.Column(db.DateTime,
            nullable=False, default=datetime.now(timezone.utc))
    # One to one relationship
    # uselist=False means that the relationship will return a 
    # single item(scalar) instead of a list of items(collection)
    addresses: Mapped['Address'] = db.relationship(
            back_populates='customers', uselist=False, lazy=True) # Lazy is true by default
    bins: Mapped['Bin'] = db.relationship(
            back_populates='customers', uselist=False)  # One to one Bin selection
    subscriptions: Mapped['Subscription'] = db.relationship(
            back_populates='customers', uselist=False)
    invoices: Mapped['Invoice'] = db.relationship(
            back_populates='customers')

    def to_dict(self) -> dict:
        """NOTE: This method can be revomed once grid.js
        (First tabular view tried) is no longer in use."""
        return {
            # CustomerDB columns
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'email': self.email,
            'cus_id': self.cus_id,
            'paymentintent_id': self.paymentintent_id,
            'active': self.active,
            'test': self.test,
            'order_date': self.order_date,
            # Address
            # Address contains the full address
            'address': self.addresses.to_dict_full_address() if self.addresses else None,
            'street': self.addresses.street_dict() if self.addresses else None,
            'city': self.addresses.city_dict() if self.addresses else None,
            'postcode': self.addresses.postcode_dict() if self.addresses else None,
            # Bin columns
            'bin_collection': self.bins.bin_collection_dict() if self.bins else None,
            'selected_bins': self.bins.selected_bins_dict() if self.bins else None,
            'clean_date': self.bins.clean_date_dict() if self.bins else None,
            # Subscription column
            'subscription': self.subscriptions.plan_dict() if self.subscriptions else None,
            # Invoice columns
            'amount_paid': self.invoices.amount_paid_dict() if self.invoices else None,
            'invoice_url': self.invoices.invoice_url_dict() if self.invoices else None,
            'inv_description': self.invoices.inv_description_dict() if self.invoices else None,
        }

    def to_json(self) -> dict:
        """Serialise the CustomerDB object to JSON"""
        json_customer = {
            # CustomerDB columns
            'url': url_for('api.get_customer', id=self.id),
            'name': self.name,
            'phone': self.phone,
            'email': self.email,
            'cus_id': self.cus_id,
            'paymentintent_id': self.paymentintent_id,
            'active': self.active,
            'test': self.test,
            'order_date': self.order_date,
            # Address
            # Address contains the full address
            'address': self.addresses.to_dict_full_address() if self.addresses else None,
            'street': self.addresses.street_dict() if self.addresses else None,
            'city': self.addresses.city_dict() if self.addresses else None,
            'postcode': self.addresses.postcode_dict() if self.addresses else None,
            # Bin columns
            'bin_collection': self.bins.bin_collection_dict() if self.bins else None,
            'selected_bins': self.bins.selected_bins_dict() if self.bins else None,
            'clean_date': self.bins.clean_date_dict() if self.bins else None,
            # Subscription column
            'subscription': self.subscriptions.plan_dict() if self.subscriptions else None,
            # Invoice columns
            'amount_paid': self.invoices.amount_paid_dict() if self.invoices else None,
            'invoice_url': self.invoices.invoice_url_dict() if self.invoices else None,
            'inv_description': self.invoices.inv_description_dict() if self.invoices else None,
        }
        return json_customer


    @staticmethod
    def from_json(json_customer) -> dict:
        """Desirialise the JSON object"""
        name = json_customer.get('name')
        if name is None or name == '':
            raise ValidationError('Customer does not have a name')
        return CustomerDB(name=name)

    def __repr__(self) -> str:
        return f'Customer {self.name}, ID: {self.id}, Phone: {self.phone}, ' \
               f'Email: {self.email}, Customer ID: {self.cus_id}, ' \
               f'PaymentIntent ID: {self.paymentintent_id}, Active: {self.active}, ' \
               f'Test: {self.test}, In ServiceM8: {self.in_serviceM8}, ' \
               f'Customer ServiceM8 ID: {self.cus_serviceM8_id}, ' \
               f'Order Date: {self.order_date}'


class Address(db.Model):
    __tablename__ = 'addresses'
    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    street: Mapped[str] = db.Column(db.String)
    city: Mapped[str] = db.Column(db.String)
    state: Mapped[str] = db.Column(db.String)
    postcode: Mapped[str] = db.Column(db.String)
    # One to one relationship
    # relationship() defines the high level relationship between two tables
    customers: Mapped['CustomerDB'] = db.relationship(back_populates='addresses', lazy=True)
    # ForeignKey() provides a low-level database constraint that ensures data integrity.
    customer_id: Mapped[int] = db.Column(db.Integer, db.ForeignKey('customers.id'))

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'street': self.street,
            'city': self.city,
            'state': self.state,
            'postcode': self.postcode
        }

    def street_dict(self) -> dict:
        return self.street

    def city_dict(self) -> dict:
        return self.city

    def postcode_dict(self) -> dict:
        return self.postcode

    def to_dict_full_address(self) -> dict:
        return self.street + ' ' + self.city \
            + ' ' + self.state + ' ' + self.postcode

    def __repr__(self) -> str:
        return f'{self.street}, \
            {self.city}, {self.state}, {self.postcode}'


class Bin(db.Model):
    __tablename__ = 'bins'
    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    bin_collection: Mapped[str] = db.Column(db.String)
    selected_bins: Mapped[str] = db.Column(db.String)
    clean_date: Mapped[str] = db.Column(db.String)
    # This will be passed the scheduling map
    clean_cycle: Mapped[str] = db.Column(db.String) # Weekly, Fortnightly, Monthly, one off  

    # One to one relationship
    customers: Mapped['CustomerDB'] = db.relationship(
        back_populates='bins', lazy=True
    )
    # ForeignKey() provides a low-level database constraint that ensures data integrity.
    customer_id: Mapped[int] = db.Column(
        db.Integer, db.ForeignKey('customers.id'),
        nullable=False
    )

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'bin_collection': self.bin_collection,
            'selected_bins': self.selected_bins,
            'clean_date': self.clean_date,
            'clean_cycle': self.clean_cycle
        }

    def bin_collection_dict(self) -> dict:
        return self.bin_collection

    def selected_bins_dict(self) -> dict:
        return self.selected_bins

    def clean_date_dict(self) -> dict:
        return self.clean_date

    def clean_cycle_dict(self) -> dict:
        return self.clean_cycle

    def __repr__(self) -> str:
        return f'Bin Collection: {self.bin_collection}, \
            Selected Bins: {self.selected_bins}'


class Subscription(db.Model):
    __tablename__ = 'subscriptions'
    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    plan: Mapped[str] = db.Column(db.String)

    # One to one relationship
    customers: Mapped['CustomerDB'] = db.relationship(back_populates='subscriptions', lazy=True)
    customer_id: Mapped[int] = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'plan': self.plan,
        }

    def plan_dict(self) -> dict:
        plan = self.plan
        if 'Subscription' in plan:
            plan = plan.replace('Subscription', '')
        return plan

    def __repr__(self) -> str:
        return f'{self.plan}'


class Invoice(db.Model):
    __tablename__ = 'invoices'
    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    invoice_id: Mapped[str] = db.Column(db.String)
    amount_paid: Mapped[str] = db.Column(db.String)
    invoice_url: Mapped[str] = db.Column(db.String)
    inv_description: Mapped[str] = db.Column(db.String)

    # One to many relationship
    customers: Mapped['CustomerDB'] = db.relationship(back_populates='invoices', lazy=True)
    customer_id: Mapped[int] = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'invoice_id': self.invoice_id,
            'amount_paid': self.amount_paid,
            'invoice_url': self.invoice_url,
            'inv_description': self.inv_description
        }

    def invoice_id_dict(self) -> dict:
        return self.invoice_id

    def amount_paid_dict(self) -> dict:
        return self.amount_paid

    def invoice_url_dict(self) -> dict:
        return self.invoice_url

    def inv_description_dict(self) -> dict:
        return self.inv_description

    def __repr__(self) -> str:
        return f'Invoice ID: {self.invoice_id}, Invoice Date: {self.invoice_date}, ' \
                f'Invoice Total: {self.invoice_total}'


class Role(db.Model):
    __tablename__ = 'roles'
    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    name: Mapped[str] = db.Column(db.String(64), unique=True)
    default: Mapped[bool] = db.Column(db.Boolean, default=False, index=True)  # Default permission
    permissions: Mapped[int] = db.Column(db.Integer)
    # One to many relationship
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __init__(self, **kwargs) -> None:  #  **kwargs accepts any number of keyword arguments
        super(Role, self).__init__(**kwargs)  # super() function returns a temporary object of the superclass that allows to call its methods
        if self.permissions is None:  # SQLALchemy will set the default value to None
            self.permissions = 0

    @staticmethod  # This method does not require an object to be created
    def insert_roles() -> None:
        """This func looks for existing roles by name.
        A new role object is created only for roles that aren’t
        in the database already. This is done so that the role
        list can be updated in the future when changes need to be made.
        To add a new role or change the permission assignments for a role,
        change the roles dictionary at the top of the function
        and then run the function again."""
        # NOTE: Roles were added via flask shell p.342
        roles = {
            'User': [Permission.USER],
            'Driver': [Permission.USER, Permission.DRIVER],
            'Admin': [Permission.USER, Permission.DRIVER, Permission.ADMIN]
        }
        default_role = 'User'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()

    def add_permission(self, perm: int) -> None:
        if not self.has_permission(perm):
            self.permissions += perm

    def reset_permissions(self) -> None:
        self.permissions = 0

    def has_permission(self, perm: int) -> bool:
        return self.permissions & perm == perm

    def __repr__(self) -> str:
        return f'Users: {self.users.email} | Name: {self.name}' \
                f'Default: {self.default} | Permissions: {self.permissions}'


class User(UserMixin, db.Model):
    """This model is to be used
    for internal authentication for
    access to the database"""
    __tablename__ = 'users'
    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    username: Mapped[str] = db.Column(db.String(64), unique=True, index=True)
    email: Mapped[str] = db.Column(db.String(120), unique=True, index=True)
    password_hash: Mapped[str] = db.Column(db.String(512))
    confirmed: Mapped[bool] = db.Column(db.Boolean, default=False)
    member_since: Mapped[datetime] = db.Column(
            db.DateTime, default=datetime.now(timezone.utc))
    last_seen: Mapped[datetime] = db.Column(
            db.DateTime, default=datetime.now(timezone.utc))
    # One to many relationship
    role_id: Mapped[int] = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __init__(self, **kwargs) -> None:
        super(User, self).__init__(**kwargs)
        """This constructor sets the role of the user
        based on email address"""
        if self.role is None:
            if self.email == current_app.config['UNITED_ADMIN']:
                self.role = Role.query.filter_by(name='Administrator').first()
            elif self.email == current_app.config['UNITED_ADMIN_1']:
                self.role = Role.query.filter_by(name='Administrator').first()
            elif self.email == current_app.config['UNITED_ADMIN_2']:
                self.role = Role.query.filter_by(name='Administrator').first()
            elif self.email == current_app.config['UNITED_ADMIN_3']:
                self.role = Role.query.filter_by(name='Administrator').first()
            elif self.email == current_app.config['UNITED_DRIVER']:
                self.role = Role.query.filter_by(name='Driver').first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()  # Defaults to 'User'

    @property  # Write-only Property decorator allows the method below to be defined as a property of an object
    def password(self) -> None:
        # AttributeError is raised if password is hashed
        # The password is not meant to be a readable attribute
        raise AttributeError('password is not a readable attribute')

    # When @password is set, the setter methods calls
    # Werrkzeug's generate_password_hash() function
    # And writes the result to the password_hash attribute
    @password.setter  # Attempting to read the password attribute raises AttributeError
    def password(self, password: str) -> None:  # As the password cannot be recovered once hashed
        self.password_hash = generate_password_hash(password)  # password_hash column from db model

    def verify_password(self, password: str) -> bool:
        """This method takes a password and passes it
        to Werkzeug's check_password_hash() function
        for verification against the hashed version
        stored in the User model, returning a True if
        password is correct"""
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600) -> str:
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token: str) -> bool:
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'), max_age=3600)
        except (BadSignature, SignatureExpired):
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id}).decode('utf-8')

    @staticmethod  # The user will be known only after token is decoded
    def reset_password(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except Exception as e:
            return f'{False} : Error: {e}'
        user = User.query.get(data.get('reset'))
        if user is None:
            return False
        user.password = new_password
        db.session.add(user)
        return True

    def generate_email_change_token(self, new_email, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps(
            {'change_email': self.id, 'new_email': new_email}).decode('utf-8')

    def change_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except Exception as e:
            return f'Error loading token:{e} {False}'
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        db.session.add(self)
        return True

    # NOTE: The below are helper methods that check
    # if a user has a particular given permission
    def can(self, perm):
        """Returns True if the user has the permission in the role"""
        return self.role is not None and self.role.has_permission(perm)

    def is_administrator(self):
        """Returns True if the user has the admin role"""
        return self.can(Permission.ADMIN)

    # Serialising the user object to JSON
    def to_json(self):
        """Email and role are omitted from response
        for privacy reasons. The representation
        of the resource offered to clients does
        not need to be identical to internal definition
        of the corresponding database model."""
        json_user = {
            'url': url_for('api.get_user', id=self.id),
            'username': self.username,
        }
        return json_user

    def ping(self):
        """Updates the last seen time of the user
        This method is called from auth/views
        and it is used to count new orders since
        last visit to be displayed on the front-end."""
        self.last_seen = datetime.now(timezone.utc)
        db.session.add(self)

    # API methods for Authentication
    def generate_auth_token(self, expiration):
        """Returns a signed token that encodes user id.
        Expiraton time is set in seconds."""
        # Create a payload with the user's ID and expiration time
        """Generate an authentication token for the user with the given expiration time in seconds."""
        try:
            payload = {
                'id': self.id,
                'exp': datetime.now(timezone.utc) + timedelta(seconds=expiration),

            }
            return jwt.encode(
                payload,
                current_app.config['SECRET_KEY'],
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def verify_auth_token(token):
        """Takes token and if valid, returns user object.
        This is a static method, the user will be known 
        only after the token is decoded."""
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        except (ExpiredSignatureError, InvalidTokenError):
            return None
        return User.query.get(data['id'])

    def __repr__(self) -> str:
        return f'User {self.username}' + ' ' +\
                f'ID: {self.id}' + ' ' +\
                f'Email: {self.email}' + ' ' + \
                f'Role_id: {self.role_id}' + ' ' + \
                f'Member Since: {self.member_since}' + ' ' + \
                f'Last Seen: {self.last_seen}'


class AnonymousUser(AnonymousUserMixin):
        """This class is created for extra convenience
        This enables the app to freely call current_user.can()
        & current_user.is_administrator() without checking
        whether the user is logged in first."""
        def can(self, permissions) -> bool:
            return False

        def is_administrator(self) -> bool:
            return False


# Tells Flask-Login to use the app's custom anonymous user
# by setting its class to the login_manager.anonymous_user attribute
login_manager.anonymous_user = AnonymousUser


# User loader function
@login_manager.user_loader
def load_user(user_id) -> int:
    """@login_manager.user_loader
    registers the function with Flask-Login
    Function is called when it needs to retrieve
    info about logged-in user"""
    return User.query.get(int(user_id))