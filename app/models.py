from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from flask import current_app
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired
from .extensions import db, login_manager


# Create association table
# https://realpython.com/python-sqlite-sqlalchemy/#table-creates-associations
# Flask Web Development 2nd Edition, p. 90


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
    # One to many relationship
    users = db.relationship('User', backref='role', lazy=True)

    def __repr__(self) -> str:
        return f'Role {self.name}'


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
    
    def __repr__(self) -> str:
        return f'User {self.username}, Email: {self.email}'


# User loader function
@login_manager.user_loader
def load_user(user_id) -> int:
    """@login_manager.user_loader
    regiters the function with Flask-Login
    Function is called when it needs to retrieve
    info about logged-in user"""
    return User.query.get(int(user_id))