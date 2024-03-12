# The app import only workds on the command line using 
# python -m app.db_operations.query_ops
# 

"""NOTE: The below does not work as it stands,
Circular import if CustomerDB and Bin Models are imported.
Can fix it by possibly moving it to models module. 
Refer to Arjan Code ABC abstraction for possible solution.

The classes below are instatiated in the extensions.py file"""

from .extensions import db
from .models import CustomerDB, Bin
#cus = 'cus_PYUAHiHNnCm0Oe'


class CustomerQuery:

    def get_customer_id(cus_id):
        """This refers to ID (primary_key)
        on the CustomerDB table"""
        customer = CustomerDB.query.filter_by(cus_id=cus_id).first()
        id = customer.id
        print(id)
        return id

    def get_cus_id(cus_id):
        """Query the customer ID from the database"""
        customer = CustomerDB.query.filter_by(cus_id=cus_id).first()
        customer_id = customer.cus_id
        print(customer_id)
        return customer_id

    def get_payment_intent(cus_id):
        """Query the payment intent ID from the database"""
        customer = CustomerDB.query.filter_by(cus_id=cus_id).first()
        payment_intent = customer.paymentintent_id
        print(payment_intent)
        return payment_intent

    def get_order_date(cus_id):
        """Query the order date from the database"""
        customer = CustomerDB.query.filter_by(cus_id=cus_id).first()
        order_date = customer.order_date
        print(order_date)
        return order_date

    def list_bins():
        """Query the bins from the database"""
        customer = CustomerDB.query.all()
        bins = customer.bins
        for customers in customer:
            for bin in bins:
                print(bin.bin_collection)
                return bin.bin_collection


class BinQuery:

    def get_bin_collection(self, id):
        """Query the bin collection from the database"""
        bin = Bin.query.filter_by(customer_id=id).first()
        bin_collection = bin.bin_collection
        print(bin_collection)
        return bin_collection

#b = BinQuery()
#bb = b.get_bin_collection(cus)


#query = CustomerQuery() # Instatiate to create the application context
#customer = query.get_customer_id(cus)
#cus_id = query.get_cus_id(cus)
#id = query.get_customer_id(cus)

#b = BinQuery()
#bb = b.get_bin_collection(id)

#intent = query.get_payment_intent(cus)


# If using functions only (not a class) use the below.
#if __name__ == '__main__':
#    app = create_app()
#    with app.app_context(): 
#        query_cus_id(cus)  # Returns the customer object with the given customer ID




#class QueryBase:
    #context for the database query operations."""
    #def __init__(self):
    #    self.app = create_app()
    #    self.app_context = self.app.app_context()
    #    self.app_context.push()  # This activates the application context

    #def __del__(self):
    #    self.app_context.pop()  # This deactivates the application context    
