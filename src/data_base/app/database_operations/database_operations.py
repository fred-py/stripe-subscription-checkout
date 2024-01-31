from models.models import CustomerDB, Address, Bin, Subscription, Invoice
from app import db


# Add new users to the Database
""""Refer to real python for with statement or arjan """
def add_customer(data):
    customer = {
        key: data[key] for key in(
            'name', 'email', 'mobile', 'cus_id', 'paymentintent_id',
        )
    }
    address = {
        key: data[key] for key in (
            'street', 'city', 'state', 'postal_code',
        )
    }
    plan = {
        key: data[key] for key in (
            'plan'
        )
    }  
    invoice = {
        key: data[key] for key in (
        'invoice_id', 'amount_paid', 'inv_description', 'invoice_url',
        )
    }
    bin = {
        key: data[key] for key in (
        'bin_collection', 'selected_bins',
        )
    }

    new_customer = CustomerDB(**customer)
    new_address = Address(**address, customer=new_customer)  # customer param links the address/customer relationship
    new_plan = Subscription(**plan, customer=new_customer)
    new_invoice = Invoice(**invoice, customer=new_customer)
    new_bin = Bin(**bin, customer=new_customer)

    db.session.add(new_customer)
    db.session.add(new_address)
    db.session.add(new_plan)
    db.session.add(new_invoice)
    db.session.add(new_bin)
