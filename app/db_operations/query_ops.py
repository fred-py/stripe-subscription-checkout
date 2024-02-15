from app import create_app
from app.models import CustomerDB
#from app.extensions import db

cus = 'cus_PYUAHiHNnCm0Oe'


class QueryOps:
    def __init__(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()  # This activates the application context

    def __del__(self):
        self.app_context.pop()  # This deactivates the application context

    def get_cus_id(self, cus_id):
        """Query the customer ID from the database"""
        customer = CustomerDB.query.filter_by(cus_id=cus_id).first()
        customer_id = customer.cus_id
        print(customer_id)
        return customer_id
    
    def get_payment_intent(self, cus_id):
        """Query the payment intent ID from the database"""
        customer = CustomerDB.query.filter_by(cus_id=cus_id).first()
        payment_intent = customer.paymentintent_id
        print(payment_intent)
        return payment_intent

#query = QueryOps() # Instatiate to create the application context
#cus_id = query.get_cus_id(cus)
#intent = query.get_payment_intent(cus)

# If using functions only (not a class) use the below.
#if __name__ == '__main__':
#    app = create_app()
#    with app.app_context(): 
#        query_cus_id(cus)  # Returns the customer object with the given customer ID