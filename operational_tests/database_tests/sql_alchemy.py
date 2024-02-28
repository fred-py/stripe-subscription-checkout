# SQLAlchemy - https://realpython.com/python-sqlite-sqlalchemy/#working-with-sqlalchemy-and-python-objects
# https://docs.sqlalchemy.org/en/20/orm/quickstart.html
# https://docs.sqlalchemy.org/en/20/tutorial/engine.html#establishing-connectivity-the-engine
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
# Base class all models inherit from
# Also how they get SQLAlchemy ORM functionality
Base = declarative_base()

# Create address association table
# https://realpython.com/python-sqlite-sqlalchemy/#table-creates-associations
"""cus_address = Table(
    'cus_address',
    Base.metadata,
    Column('id', Integer, ForeignKey('customer.id')),  # id from Customer Class
    Column('address_id', Integer, ForeignKey('address.address_id')),
    Column('sub_id', Integer, ForeignKey('subscription.sub_id')),
)"""

ad_subscription = Table(
    'ad_subscription',
    Base.metadata,
    Column('id', Integer, ForeignKey('customer.id')),
    Column('sub_id', Integer, ForeignKey('subscription.sub_id')),
    Column('address_id', Integer, ForeignKey('address.address_id')),
)

cus_subscription = Table(
    'cus_subscription',
    Base.metadata,
    Column('id', Integer, ForeignKey('customer.id')),
    Column('sub_id', Integer, ForeignKey('subscription.sub_id')),
    Column('address_id', Integer, ForeignKey('address.address_id')),
)


# Customer Model
class Customer(Base):
    __tablename__ = 'customer' # Dunder method specifies the table it belongs to
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    phone = Column(String)
    email = Column(String)
    cus_id = Column(String)  # Stripe customer ID
    bin_collection = Column(String)  # For on-going cleans
    selected_bins = Column(String)  # For bronze and one-off cleans
    clean_date = Column(String)  # For one off-cleans
    active = Column(Boolean, default=True)  # False if customer cancels subscription
    test = Column(Boolean, default=False)  # If test customer bool=True
    in_serviceM8 = Column(Boolean, default=False)  # If customer is in ServiceM8

    addresses = relationship(
        'Address',
        #backref=backref('customer'),
        #cascade='all, delete-orphan',

        secondary=ad_subscription,
        back_populates='customers',
    )

    subscriptions = relationship(
        'Subscription',
        secondary=cus_subscription,
        back_populates='customers'
    )

    def __repr__(self):
        # !r in the string formatting syntax {self.id!r} is used
        # to call repr() on self.id before formatting it
        # into the string. The repr() function returns a
        # string that represents a printable version of an object.
        # This can be useful for debugging, as it includes more detail
        # about the object than str().
        return (
            f'Customer(id={self.id!r},'
            f'first_name={self.first_name!r},'
            f'last_name={self.last_name!r},'
            f'phone={self.phone!r},'
            f'email={self.email!r},'
            f'cus_id={self.cus_id!r},'
            f'bin_collection={self.bin_collection!r},'
            f'selected_bins={self.selected_bins!r},'
            f'clean_date={self.clean_date!r},'
            f'active={self.active!r},'
        )


# Address Model
class Address(Base):
    __tablename__ = 'address'
    address_id = Column(Integer, primary_key=True)
    street = Column(String)
    city = Column(String)
    state = Column(String)
    postcode = Column(String)
    # id from Customer Class
    # Foreign key allows us to create queries linking the object
    # both forwards and backwards inside the Address objects
    # Inside the Address object we can access the customer details
    # linked to the address 
    id = Column(Integer, ForeignKey('customer.id'))
    #current_customer_id = Column(Integer, ForeignKey("customer.id"))

    #customers = relationship(
    #    'Customer',
    #    secondary=cus_address,
    #    back_populates='addresses'
    #)
    # This flag indicates which customer is 
    #currently subscribed and living at the addess
    #current_customer = relationship(
    #    'Customer',
    #    backref='current_address',
    #)

    subscriptions = relationship(
        'Subscription',
        secondary=cus_subscription,
        back_populates='addresses'
    )


# Subscription Model
class Subscription(Base):
    __tablename__ = 'subscription'
    sub_id = Column(Integer, primary_key=True)
    plan = Column(String)
    total_paid = Column(String)
    active = Column(Boolean, default=True)  # False if customer cancels subscription or changes plan
    # id from Customer Class
    # Refer to comments on Address Model for more information
    #id = Column(Integer, ForeignKey('customer.id'))
    
    # This object represents the actual 
    # subscription, the relationship
    # Declare relationship to the Customer 
    # and Address models using the secondary tables
    # defined above 
    customers = relationship(
        'Customer',
        secondary=cus_subscription,
        back_populates='subscriptions'
    )
    addresses = relationship(
        'Address',
        secondary=ad_subscription,
        back_populates='subscriptions'
    )


# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
# https://docs.sqlalchemy.org/en/20/tutorial/engine.html#establishing-connectivity-the-engine
engine = create_engine('sqlite:///sqlalchemy_test.db')

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)

# Create a Session class bound to the engine
Session = sessionmaker(bind=engine)

# Create an instance of the Session class
session = Session()

"""Query examples"""
# Create statemet
#stmt = select(Subscription)
# Scalars method is used instread of execute to 
# query all the customers in the database
#for customers in session.scalars(stmt):
#    print(customers)

"""stmt = select(Customer).join(Address.postcode).where(Address.postcode == '6085')
for customer in session.scalars(stmt):
    print(customer)"""

"""
stmt = select(Customer).where(Customer.first_name == 'Fred')
fred = session.scalars(stmt).one() # .one() returns one result
"""
results = session.query(Customer).all()
print(results)