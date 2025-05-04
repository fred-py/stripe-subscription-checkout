import timeit
import os
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
    #amount_paid: int
    #inv_description: str
    #invoice_url: str
    # => Bin details
    bin_collection: str
    selected_bins: str


def prepare_session_data(data) -> dict:
    """Prepare data from checkout session
    Test is omitted on production, if testing, set to True"""
    # => Customer Details
    name = data['customer']['name']
    email = data['customer']['email']
    phone = data['customer']['phone']
    cus_id = data['customer']['id']
    #paymentintent_id = data['customer']['metadata']['paymentintent_id']
    # => Address Details
    street = data['customer']['address']['line1']
    city = data['customer']['address']['city']
    state = data['customer']['address']['state']
    postcode = data['customer']['address']['postal_code']
    # => Subscription Details
    plan = data['subscription']['plan_type']
    # => Invoice Details
    #invoice_id = data['customer']['metadata']['invoice_id']
    #amount_paid = int(data['customer']['metadata']['amount_paid'])
    #amount_paid = (amount_paid / 100) # Convert cents to dollars
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
        #'paymentintent_id': paymentintent_id,
        # Address Model
        'street': street,
        'city': city,
        'state': state,
        'postcode': postcode,
        # Subscription Model
        'plan': plan,
        # Invoice Model
        #'invoice_id': invoice_id,
        #'amount_paid': amount_paid,
        #'inv_description': inv_description,
        #'invoice_url': invoice_url,
        # Bin Model
        'bin_collection': bin_collection,
        'selected_bins': selected_bins,
    }


"""The below had been added for future testing only
when the module is run directly"""
def main() -> None:
    customer_data = prepare_session_data(data)
    customer = Customer(**customer_data)  # ** Unpacks dict
    print(customer)

if __name__ == "__main__":
    main()



# SAMPLE JSON CHECKOUT RESPONSE
# data2 = {'customer': <Customer customer id=cus_PTFx24gnUM1XiE at 0x105321850> JSON: {
#   "address": {
#     "city": "Margaret River",
#     "country": "AU",
#     "line1": "20 Humble Way",
#     "line2": null,
#     "postal_code": "6285",
#     "state": "WA"
#   },
#   "balance": 0,
#   "created": 1706629339,
#   "currency": "aud",
#   "default_currency": "aud",
#   "default_source": null,
#   "delinquent": false,
#   "description": null,
#   "discount": null,
#   "email": "rezende.f@outlook.com",
#   "id": "cus_PTFx24gnUM1XiE",
#   "invoice_prefix": "E5F7C29E",
#   "invoice_settings": {
#     "custom_fields": null,
#     "default_payment_method": null,
#     "footer": null,
#     "rendering_options": null
#   },
#   "livemode": false,
#   "metadata": {
#     "paymentintent_id": "pi_3OeJS4L0FB5xAf6H1qfR3f4q"
#   },
#   "name": "Kweoa eoaifjiopefj p",
#   "next_invoice_sequence": 2,
#   "object": "customer",
#   "phone": "+61404741268",
#   "preferred_locales": [
#     "en-GB"
#   ],
#   "shipping": null,
#   "tax_exempt": "none",
#   "test_clock": null
# }, 'subscription': {'amount_paid': 21600, 'plan_type': 'Gold Subscription'}, 'booking_details': [<StripeObject at 0x105322090> JSON: {
#   "dropdown": {
#     "options": [
#       {
#         "label": "Monday",
#         "value": "monday"
#       },
#       {
#         "label": "Tuesday",
#         "value": "tuesday"
#       },
#       {
#         "label": "Wednesday",
#         "value": "wednesday"
#       },
#       {
#         "label": "Thursday",
#         "value": "thursday"
#       },
#       {
#         "label": "Friday",
#         "value": "friday"
#       }
#     ],
#     "value": "thursday"
#   },
#   "key": "collection_date",
#   "label": {
#     "custom": "Bin Collection Day",
#     "type": "custom"
#   },
#   "optional": false,
#   "type": "dropdown"
# }]}


# ======== THE BELOW ARE NOT IN USE ========= # 

"""====> THIS FUNC IS NOT IN USE ON THIS MODULE*****"""
def prepare_data(data) -> dict:
    # Concatnate address for Servicem8
    full_address = data['customer']['address']['line1'] + ' ' + \
        data['customer']['address']['city'] + ' ' + \
        data['customer']['address']['state'] + ' ' + \
        data['customer']['address']['postal_code']
    # City and Postal Code will be passed to the db
    city = data['customer']['address']['city']
    postal_code = data['customer']['address']['postal_code']
    plan = data['subscription']['plan_type']  # Subscription Plan
    bin_collection = data['booking_details'][0]['dropdown']['value']
    total_paid = data['subscription']['amount_paid']
    # Convert cents to dollars & int to str
    total_paid = str(total_paid / 100)
    name = data['customer']['name']
    email = data['customer']['email']
    mobile = data['customer']['phone']

    """Check plan type, if Bronze or Any Combo (One-Off),
    bin selection is passed to Servicem8 description"""
    plan = data['subscription']['plan_type']  # Subscription Plan
    if plan == 'Bronze' or plan == 'One-Off':
        selected_bins = data['booking_details'][0]['dropdown']['value']
        description = plan + ' | ' + \
            bin_collection + '  ' +  \
            f'| Total paid: ${total_paid}' + ' ' + \
            f'| Selected Bin(s): {selected_bins}'

    else:
        # Concatnate info to go on job description
        description = plan + ' | ' \
            + bin_collection + ' ' \
            + f' | Total paid: ${total_paid}' 
    # Dict is unpacked when instantiating Customer Class
    return {
        'full_address': full_address,
        'city': city,
        'postal_code': postal_code,
        'plan': plan,
        'bin_collection': bin_collection,
        'total_paid': total_paid,
        'name': name,
        'email': email,
        'mobile': mobile,
        'description': description,
    }
"""Class not currenlty in use, refer to data_transfer module
for servicem8 class currently in use"""
class ServiceM8:

    ups = os.getenv('UPS_KEY')

    def __init__(self, data: dict, servicem8_key: str) -> None:
        self.data = data
        self.servicem8_key = servicem8_key

    def create_job(self) -> str:
        """Uses checkout data to create 
        new job on ServiceM8."""
        # Check which key is being used
        plan = self.customer.plan  # Subscription Plan
        if self.servicem8_key == self.ups and plan == 'One-Off':
            # This ensures One-Off jobs are not passed
            # to main ServiceM8 account
            pass
        else:
            # Concatnate address
            address = self.customer.full_address
            plan = self.customer.plan  # Subscription Plan
            bin_collection = self.customer.bin_collection
            total_paid = self.customer.total_paid  # Total Amount
            # Convert cents to dollars & int to str
            total_paid = str(total_paid / 100)
            """Check plan type, if Bronze or Any Combo (One-Off),
            bin selection is passed to Servicem8 description"""
            plan = self.data['subscription']['plan_type']  # Subscription Plan
            if plan == 'Bronze' or plan == 'One-Off':
                selected_bins = self.data['booking_details'][1]['dropdown']['value']
                description = plan + ' | ' + \
                    bin_collection + '  ' +  \
                    f'| Total paid: ${total_paid}' + ' ' + \
                    f'| Selected Bin(s): {selected_bins}'

            else:
                # Concatnate info to go on job description
                description = plan + ' | ' \
                    + bin_collection + ' ' \
                    + f' | Total paid: ${total_paid}'

            # Create new job
            url = "https://api.servicem8.com/api_1.0/job.json"

            # Ensure jobs created under ups servicem8 account
            # are marked as unsuccessful
            if self.servicem8_key == self.ups:
                job_status = 'Unsuccessful'
            else:
                job_status = 'Quote'

            payload = {
                "active": 1,
                "job_address": address,
                "geo_country": "Australia",
                "geo_state": "Western Australia",
                "status": job_status,
                "job_description": description,
                "total_invoice_amount": total_paid,
                "invoice_sent": "yes",
                "payment_processed": "yes",
            }
            headers = {
                "accept": "application/json",
                "content-type": "application/json",
                # Fl0 does not take Env Variables with empty spaces
                # Therefore, Basic + ' ' + key is required
                "authorization": 'Basic' + ' ' + self.servicem8_key,
                "uuid": "x-record-uuid"
            }

            try:
                response = requests.post(url, json=payload, headers=headers)
                print(f'create_job: {response.text}')
                # Get job uuid to attached contact to job
                job_uuid = response.headers['x-record-uuid']
                return job_uuid
            except Exception as e:
                raise (e)

    def create_contact(self, job_uuid: str) -> None:
        """Uses data from checkout session
        & job_uuid returned from create_job func
        to create new job contact on ServiceM8,
        attached to job_uuid."""

        name = self.data['customer']['name']
        email = self.data['customer']['email']
        mobile = self.data['customer']['phone']
        url = "https://api.servicem8.com/api_1.0/jobcontact.json"
        # Create new job contact
        payload = {
            "active": 1,
            "job_uuid": job_uuid,
            "first": name,
            #"last": name2,
            "email": email,
            "mobile": mobile,
            "type": "Job Contact",
            "is_primary_contact": "yes",
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            # Fl0 does not take Env Variables with empty spaces
            # Therefore, Basic + ' ' + key is required
            "authorization": 'Basic' + ' ' + self.servicem8_key,
        }
        try:
            response = requests.post(url, json=payload, headers=headers)
            print(f'create_contact: {response.text}')
        except Exception as e:
            raise (e)
