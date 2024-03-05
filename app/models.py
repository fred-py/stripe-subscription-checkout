from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from flask import current_app
from flask_login import UserMixin, AnonymousUserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired
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
    order_date: Mapped[datetime] = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # One to one relationship
    # uselist=False means that the relationship will return a 
    # single item(scalar) instead of a list of items(collection)
    addresses: Mapped['Address'] = db.relationship(back_populates='customers', uselist=False, lazy=True) # Lazy is true by default
    # One to one Bin selection
    bins: Mapped['Bin'] = db.relationship(back_populates='customers', uselist=False)
    # One to one relationship
    subscriptions: Mapped['Subscription'] = db.relationship(back_populates='customers', uselist=False)
    # One to many relationship
    invoices: Mapped['Invoice'] = db.relationship(back_populates='customers')

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

    def __repr__(self) -> str:
        return f'Address {self.street}, {self.city}, {self.state}, {self.postcode}, ' \
                f'Customer ID: {self.customer_id}, ' \
                f'Customer: {self.customers}'


class Bin(db.Model):
    __tablename__ = 'bins'
    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    bin_collection: Mapped[str] = db.Column(db.String)
    selected_bins: Mapped[str] = db.Column(db.String)
    clean_date: Mapped[str] = db.Column(db.String)
    # This will be passed the scheduling map
    clean_cycle: Mapped[str] = db.Column(db.String) # Weekly, Fortnightly, Monthly, one off  

    # One to one relationship
    customers: Mapped['CustomerDB'] = db.relationship(back_populates='bins', lazy=True)
    # ForeignKey() provides a low-level database constraint that ensures data integrity.
    customer_id: Mapped[int] = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)

    def __repr__(self) -> str:
        return f'Bin Collection: {self.bin_collection}, Selected Bins: {self.selected_bins}, ' \
                f'Clean Date: {self.clean_date}, Clean Cycle: {self.clean_cycle}, ' \
                f'Customer ID: {self.customer_id}, ' \
                f'Customer: {self.customers}'


class Subscription(db.Model):
    __tablename__ = 'subscriptions'
    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    plan: Mapped[str] = db.Column(db.String)
    active: Mapped[bool] = db.Column(db.Boolean, default=True)

    # One to one relationship
    customers: Mapped['CustomerDB'] = db.relationship(back_populates='subscriptions', lazy=True)
    customer_id: Mapped[int] = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)

    def __repr__(self) -> str:
        return f'Subscription Plan: {self.plan}, Total Paid: {self.total_paid}, ' \
                f'Active: {self.active}, Customer ID: {self.customer_id}, ' \
                f'Customer: {self.customers}'


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

    def __repr__(self) -> str:
        return f'Invoice ID: {self.invoice_id}, Invoice Date: {self.invoice_date}, ' \
                f'Invoice Total: {self.invoice_total}, Customer ID: {self.customer_id}, ' \
                f'Customer: {self.customers}'


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
        return '<Role %r>' % self.name


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

    def generate_confirmation_token(self) -> str:
        s = Serializer(current_app.config['SECRET_KEY'])
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

    @staticmethod
    def reset_password(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
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

    def __repr__(self) -> str:
        return '<User %r>' % self.username, self.email


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