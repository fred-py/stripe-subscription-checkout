# https://developer.servicem8.com/reference/post-jobcontact-create
import requests
import os 
from dotenv import load_dotenv, find_dotenv
from .customer import add_customer  # Relative import with . as NoModuleError was being raised
import time
import asyncio


load_dotenv(find_dotenv())


async def create_job(data, servicem8_key):
    """Extract json data & creates new job on ServiceM8.
    This function runs in parallel with the main program
    so checkout process speed is not affected."""
    ups = os.getenv('UPS_KEY')  # ServiceM8 United Property Services Keys
    start_time = time.time()

    # Check which key is being used
    plan = data['subscription']['plan_type']  # Subscription Plan
    if servicem8_key == ups and plan == 'One-Off':
        # This ensures One-Off jobs are not created for main ServiceM8 account
        pass
    else:
        # Concatnate address
        address = data['customer']['address']['line1'] + ' ' + \
            data['customer']['address']['city'] + ' ' + \
            data['customer']['address']['state'] + ' ' + \
            data['customer']['address']['postal_code']
        plan = data['subscription']['plan_type']  # Subscription Plan
        # Custom_field is a list of dicts
        # therefore 0 index is required to access the dict
        # then access the key 'dropdown' which is a dict and so forth
        # Using param custom field directly for ease of use
        bin_collection = data['bin_collection']
        total_paid = data['subscription']['amount_paid']  # Total Amount
        # Convert cents to dollars & int to str
        total_paid = str(total_paid / 100)
        """Check plan type, if Bronze or Any Combo (One-Off),
        bin selection is passed to Servicem8 description"""
        plan = data['subscription']['plan_type']  # Subscription Plan
        if plan == 'Bronze Subscription' or plan == 'One-Off':
            selected_bins = data['selected_bins']
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

        payload = {
            "active": 1,
            "job_address": address,
            "geo_country": "Australia",
            "geo_state": "Western Australia",
            "status": "Quote",
            "job_description": description,
            "total_invoice_amount": total_paid,
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
            print(f'create_job: {response.text}')
            # Get job uuid to attached contact to job
            job_uuid = response.headers['x-record-uuid']
            duration = time.time() - start_time
            print(f'Duration for job {servicem8_key, job_uuid} is {duration}', time.strftime("%H:%M:%S", time.localtime(start_time)))
            await create_contact(job_uuid, data, servicem8_key)
        except Exception as e:
            print(e)


async def create_contact(job_uuid, data, servicem8_key):
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
        #add_customer(mobile, name, servicem8_key)
        print(f'create_contact: {response.text}')
    except Exception as e:
        print(e)


if __name__ == '__main__':
    create_job()



# United Property ServiceM8 API Key: 'Basic cmV6ZW5kZS5mQG91dGxvb2suY29tOmQzNDQyZWY2LTk1MmUtNGI1Ny05Mzc0LTIwNTgxN2FhZjg2Yg=='


