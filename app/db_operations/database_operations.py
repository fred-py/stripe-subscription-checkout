from app.models import CustomerDB, Address, Bin, Subscription, Invoice
from app.extensions import db


# Add new users to the Database
""""Refer to real python for with statement or arjan """
def add_user(data):
    # Customer details from Customer Dataclass
    name = data.name
    email = data.email
    phone = data.phone
    cus_id = data.cus_id
    paymentintent_id = data.paymentintent_id
    
    # Address
    street = data.street
    city = data.city
    state = data.state
    postcode = data.postcode
    
    # Plan
    plan = data.plan

    # Invoice Details
    invoice_id = data.invoice_id,
    amount_paid = data.amount_paid
    inv_description = data.inv_description,
    invoice_url = data.invoice_url,

    # Bin information
    bin_collection = data.bin_collection
    selected_bins = data.selected_bins
    
    new_user = CustomerDB(
        name=name,
        email=email,
        phone=phone,
        cus_id=cus_id,
        paymentintent_id=paymentintent_id,
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
        invoice_id=invoice_id,
        amount_paid=amount_paid,
        inv_description=inv_description,
        invoice_url=invoice_url,
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


