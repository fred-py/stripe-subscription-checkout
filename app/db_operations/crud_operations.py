from app.models import CustomerDB, Address, LeadAddress, \
    Bin, Subscription, Invoice, Lead, OneOffRes, Commercial
from app.extensions import db
from ..emails import send_error_email
import logging

def add_user(data, test=False):
    # Add new users to the Database
    """"Refer to real python for with statement or arjan """
    
    #print(f'*** Data received from add_user function: => *** {data}')
    try:
        # Customer details from Customer Dataclass
        name = data.name
        email = data.email
        phone = data.phone
        cus_id = data.cus_id
        #paymentintent_id = data.paymentintent_id
        test = test
        
        # Address
        street = data.street
        city = data.city
        state = data.state
        postcode = data.postcode
        
        # Plan
        plan = data.plan

        # Invoice Details
        #invoice_id = data.invoice_id,
        amount_paid = data.amount_paid
        #inv_description = data.inv_description,
        #invoice_url = data.invoice_url,

        # Bin information
        bin_collection = data.bin_collection
        selected_bins = data.selected_bins
        
        new_user = CustomerDB(
            name=name,
            email=email,
            phone=phone,
            cus_id=cus_id,
            #paymentintent_id=paymentintent_id,
            test=test,
        )

        new_address = Address(
            street=street,
            city=city,
            state=state,
            postcode=postcode,
            customers=new_user,  # customer param links the address/customer relationship
        )

        new_plan = Subscription(
            plan=plan,
            customers=new_user,  # Creates relationship with customer
        )

        new_invoice = Invoice(
            #invoice_id=invoice_id,
            amount_paid=amount_paid,
            #inv_description=inv_description,
            #invoice_url=invoice_url,
            customers=new_user,
        )

        new_bin = Bin(
            bin_collection=bin_collection,
            selected_bins=selected_bins,
            customers=new_user,
        )
        db.session.add(new_user)
        db.session.add(new_address)
        db.session.add(new_plan)
        db.session.add(new_invoice)
        db.session.add(new_bin)

        db.session.commit()
        print('All good')
    except Exception as e:
        db.session.rollback()  # IMPORTANT: Rollback changes if an error occurs
        logging.error(f'Error adding new user to the database: {e}', exc_info=True) # exc_info for traceback
        try:
            send_error_email(error_message=str(e))
        except Exception as email_err:
            logging.error(f'Failed to send email: {email_err}')
            raise Exception(f'Error adding new user to the database: {e}')


def add_one_off_user(data, test=False):
    """Add one-off residential enquiries
    to the database."""
    # Data refers to data dictionary from wtf form
    # Lead Model
    name = data['name']
    email = data['email']
    phone = data['mobile']
    service = data['service']
    message = data['message']

    # Address in the same model
    street = data['street']
    city = data['city']
    postcode = data['postcode']

    res_enquiry = OneOffRes(
        name=name,
        email=email,
        phone=phone,
        service=service,
        message=message,
        street=street,
        city=city,
        postcode=postcode,
        test=test
    )

    db.session.add(res_enquiry)
    db.session.commit()
    return res_enquiry


def add_commercial(data, test=False):
    """Add commercial enquiries
    to the database."""
    # Data refers to data dictionary from wtf form
    # Lead Model
    name = data['name']
    email = data['email']
    phone = data['mobile']
    service = data['service']
    message = data['message']

    # Address in the same model
    street = data['street']
    city = data['city']
    postcode = data['postcode']

    comm_enquiry = Commercial(
        name=name,
        email=email,
        phone=phone,
        service=service,
        message=message,
        street=street,
        city=city,
        postcode=postcode,
        test=test
    )

    db.session.add(comm_enquiry)
    db.session.commit()
    return comm_enquiry


def add_lead(data, test=False):
    """Add one-off to the database.
    Those who register their interest"""
    # Data refers to data dictionary from wtf form
    # Lead Model
    name = data['name']
    email = data['email']
    phone = data['mobile']
    service = data['service']


    # Address Model
    street = data['street']
    city = data['city']
    postcode = data['postcode']

    new_lead = Lead(
        name=name,
        email=email,
        phone=phone,
        service=service,
        test=test
    )

    address = LeadAddress(
        street=street,
        city=city,
        postcode=postcode,
        leads=new_lead,  # customer param links the address/lead relationship
    )
    db.session.add(new_lead)
    db.session.add(address)
    db.session.commit()
    return new_lead


def get_email(email, model=None):
    """By default this function returns Lead
    details by querying the email
    If model=Customer the function will return
    email from CustomerDB Model """
    data = email.strip()  # Remove leading/trailing spaces
    if model is None:
        lead = Lead.query.filter_by(email=data).first()
        return lead
    elif model == 'commercial':
        c = Commercial.query.filter_by(email=data).first()
        return c
    elif model == 'residential':
        r = OneOffRes.query.filter_by(email=data).first()
        return r
    elif model == 'customer':
        e = CustomerDB.query.filter_by(email=data).first()
        return e
