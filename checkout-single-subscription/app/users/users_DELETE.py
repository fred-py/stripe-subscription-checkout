from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from datetime import datetime
from app import db

# Create association table
# https://realpython.com/python-sqlite-sqlalchemy/#table-creates-associations


class Customer(db.Model):
    __tablename__ = 'customer'
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
    addresses: Mapped['Address'] = db.relationship(back_populates='customer', uselist=False, lazy=True) # Lazy is true by default
    # One to one Bin selection
    bins: Mapped['Bin'] = db.relationship(back_populates='customer', uselist=False)
    # One to one relationship
    subscriptions: Mapped['Subscription'] = db.relationship(back_populates='customer', uselist=False)
    # One to many relationship
    invoices: Mapped['Invoice'] = db.relationship(back_populates='customer')

    def __repr__(self) -> str:
        pass


class Address(db.Model):
    __tablename__ = 'address'
    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    street: Mapped[str] = db.Column(db.String)
    city: Mapped[str] = db.Column(db.String)
    state: Mapped[str] = db.Column(db.String)
    postcode: Mapped[str] = db.Column(db.String)
    
    # One to one relationship
    # relationship() defines the high level relationship between two tables
    customers: Mapped['Customer'] = db.relationship(back_populates='address', lazy=True)
    # ForeignKey() provides a low-level database constraint that ensures data integrity.
    customer_id: Mapped[int] = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)


class Bin(db.Model):
    __tablename__ = 'bin'
    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    bin_collection: Mapped[str] = db.Column(db.String)
    selected_bins: Mapped[str] = db.Column(db.String)
    clean_date: Mapped[str] = db.Column(db.String)
    # This will be passed the scheduling map
    clean_cycle: Mapped[str] = db.Column(db.String) # Weekly, Fortnightly, Monthly, one off  

    # One to one relationship
    customers: Mapped['Customer'] = db.relationship(back_populates='bin', lazy=True)
    # ForeignKey() provides a low-level database constraint that ensures data integrity.
    customer_id: Mapped[int] = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)


class Subscription(db.Model):
    __tablename__ = 'subscription'
    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    plan: Mapped[str] = db.Column(db.String)
    total_paid: Mapped[str] = db.Column(db.String)
    active: Mapped[bool] = db.Column(db.Boolean, default=True)

    # One to one relationship
    customers: Mapped['Customer'] = db.relationship(back_populates='subscription', lazy=True)
    customer_id: Mapped[int] = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)


class Invoice(db.Model):
    __tablename__ = 'invoice'
    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    invoice_id: Mapped[str] = db.Column(db.String)
    invoice_date: Mapped[str] = db.Column(db.String)
    invoice_total: Mapped[str] = db.Column(db.String)
    
    # One to many relationship
    customers: Mapped['Customer'] = db.relationship(back_populates='invoice', lazy=True)
    customer_id: Mapped[int] = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)


if __name__ == '__main__':
    db.create_all()
    print('Database created')