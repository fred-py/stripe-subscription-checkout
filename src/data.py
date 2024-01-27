import timeit
import os
from dataclasses import dataclass
from functools import partial
from statistics import median

"""Improve the Performance of Accessing Class Members
With Slots"""


data = {
        'customer': {
            'address': {
                'line1': '123 Main St',
                'city': 'New York',
                'state': 'NY',
                'postal_code': '10001'
            },
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'phone': '1234567890'
        },
        'subscription': {
            'plan_type': 'Bronze',
            'amount_paid': 2300  # Random amount between 1000 and 5000 cents
        },
        'booking_details': [
            {
                'dropdown': {
                    'value': 'Option 1',
                },
                'dropdown2': {
                    'value': 'Option 2',
                }
            }
        ]
    }

# When slots are set to True the objects will be created 
# using slots instead of the traditional dictionary
@dataclass(slots=True)
class Customer:
    name: str
    full_address: str
    city: str
    postal_code: str
    email: str
    mobile: str
    plan: str
    bin_collection: str
    total_paid: str
    description: str
    cus_id: str = None


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


def main() -> None:
    customer_data = prepare_data(data)
    customer = Customer(**customer_data)  # ** Unpacks dict
    print(customer)


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






# uncomment the class below that uses multiple inheritance and see the error
# class PersonEmployee(PersonSlots, EmployeeSlots):
#    pass


"""def get_set_delete(person: Person | PersonSlots):
    person.address = "123 Main St"
    person.address
    del person.address


def main():
    person = Person("John", "123 Main St", "john@doe.com")
    person_slots = PersonSlots("John", "123 Main St", "john@doe.com")
    no_slots = median(timeit.repeat(partial(get_set_delete, person), number=1000000))
    slots = median(timeit.repeat(partial(get_set_delete, person_slots), number=1000000))
    print(f"No slots: {no_slots}")
    print(f"Slots: {slots}")
    print(f"% performance improvement: {(no_slots - slots) / no_slots:.2%}")"""


if __name__ == "__main__":
    main()
