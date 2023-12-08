# https://developer.servicem8.com/reference/post-jobcontact-create
import requests
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


def create_job(info, customer, custom_field, servicem8_key):
    """Extract json data & creates new job on ServiceM8."""

    data = {'info': info, 'customer': customer, 'custom_filed': custom_field}
    # Concatnate address
    address = data['customer']['address']['line1'] + ' ' + \
        data['customer']['address']['city'] + ' ' + \
        data['customer']['address']['state'] + ' ' + \
        data['customer']['address']['postal_code']
    job_description = data['info'][1]  # Subscription Plan
    # Custom_field is a list of dicts
    # therefore 0 index is required to access the dict
    # then access the key 'dropdown' which is a dict and so forth
    # Using param custom field directly for ease of use
    bin_collection = custom_field[0]['dropdown']['value']
    invoice_amount = data['info'][0]  # Total Amount
    # Convert cents to dollars & int to str
    invoice_amount = str(invoice_amount / 100)

    """Check plan type, if Bronze or Any Combo (One-Off),
    bin selection is passed to Servicem8 description"""
    value = info[1]
    if value == 'Bronze Subscription' or value == 'Any Combo':
        selected_bins = custom_field[1]['dropdown']['value']
        description = job_description + ' ' \
            + bin_collection + ' ' \
            + f'Total paid: ${invoice_amount}' + ' ' \
            + f'Selected Bin(s): {selected_bins}'

    else:
        # Concatnate info to go on job description
        description = job_description + ' ' \
            + bin_collection + ' ' \
            + f'Total paid: ${invoice_amount}'

    # Create new job
    url = "https://api.servicem8.com/api_1.0/job.json"

    payload = {
        "active": 1,
        "job_address": address,
        "geo_country": "Australia",
        "geo_state": "Western Australia",
        "status": "Quote",
        "job_description": description,
        "total_invoice_amount": invoice_amount,
        "invoice_sent": "yes",
        "payment_processed": "yes",
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": servicem8_key,
        "uuid": "x-record-uuid"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        print(response.text)
        # Get job uuid to attached contact to job
        job_uuid = response.headers['x-record-uuid']
        create_contact(job_uuid, data, servicem8_key)

    except Exception as e:
        print(e)    


def create_contact(job_uuid, data, servicem8_key):
    """Extract json data & creates
    new job contact on ServiceM8."""

    name = data['customer']['name']
    email = data['customer']['email']
    mobile = data['customer']['phone']
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
        "authorization": servicem8_key,
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        return f'create_contact: {response.text}'
    except Exception as e:
        print(e)


if __name__ == '__main__':
    create_job()



# United Property ServiceM8 API Key: 'Basic cmV6ZW5kZS5mQG91dGxvb2suY29tOmQzNDQyZWY2LTk1MmUtNGI1Ny05Mzc0LTIwNTgxN2FhZjg2Yg=='
