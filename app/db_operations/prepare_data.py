import timeit
import os
import json
from dataclasses import dataclass
from functools import partial
from statistics import median




"""Improve the Performance of Accessing Class Members
With Slots"""


# When slots are set to True the objects will be created 
# using slots instead of the traditional dictionary
@dataclass(slots=True)
class Customer:
    name: str
    email: str
    phone: str
    cus_id: str
    #paymentintent_id: str
    # => Address Details
    street: str
    city: str
    state: str
    postcode: str
    # => Subscription Details
    plan: str
    # => Invoice Details
    #invoice_id: str
    amount_paid: int
    #inv_description: str
    #invoice_url: str
    # => Bin details
    bin_collection: str
    selected_bins: str


def prepare_session_data(data) -> dict:
    """Prepare data from checkout session
    Test is omitted on production, if testing, set to True"""
    try:
        # => Customer Details
        name = data['customer']['name']
        email = data['customer']['email']
        phone = data['customer']['phone']
        cus_id = data['customer']['id']
        #payment_intent_id = data['customer']['metadata']['payment_intent']
        # => Address Details
        street = data['customer']['address']['line1']
        city = data['customer']['address']['city']
        state = data['customer']['address']['state']
        postcode = data['customer']['address']['postal_code']
        # => Subscription Details
        plan = data['subscription']['plan_type']
        # => Invoice Details
        #invoice_id = data['customer']['metadata']['invoice_id']
        amount_paid = int(data['subscription']['amount_paid'])
        amount_paid = (amount_paid / 100) # Convert cents to dollars
        #inv_description = data['customer']['metadata']['inv_description']
        #invoice_url = data['customer']['metadata']['invoice_url']
        # => Bin details
        bin_collection = data['booking_details'][0]['dropdown']['value']
        """Check plan type, if Bronze or Any Combo (One-Off),
        bin selection is passed to Servicem8 description"""
        if plan == 'Bronze' or plan == 'One-Off':
            selected_bins = data['booking_details'][0]['dropdown']['value']
        else:
            selected_bins = 'N/A'

        return {
            # Customer model
            'name': name,
            'email': email,
            'phone': phone,
            'cus_id': cus_id,
            #'payment_intent_id': payment_intent_id,
            # Address Model
            'street': street,
            'city': city,
            'state': state,
            'postcode': postcode,
            # Subscription Model
            'plan': plan,
            # Invoice Model
            #'invoice_id': invoice_id,
            'amount_paid': amount_paid,
            #'inv_description': inv_description,
            #'invoice_url': invoice_url,
            # Bin Model
            'bin_collection': bin_collection,
            'selected_bins': selected_bins,
        }
    except Exception as e:
        raise f'Error processing data with prepare_session_data function: => {e}'


def open_json(file_path) -> dict:
    """This is a helper function 
    for testing purposes only"""
    with open(file_path, mode='r', encoding='utf-8') as r:
        data = json.load(r)
        
        return data


def main() -> None:
    """This main function is to be used for testing only
    when the module is run directly"""
    data = open_json('stripe_invoice_paid_data.json')
    print(data)
    customer_data = prepare_session_data(data)
    customer = Customer(**customer_data)  # ** Unpacks dict
    print(customer)


if __name__ == "__main__":
    main()