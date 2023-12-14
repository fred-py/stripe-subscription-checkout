# https://developer.servicem8.com/reference/post-jobcontact-create
import requests
import os 
from dotenv import load_dotenv, find_dotenv
#from .customer import add_customer  # Relative import with . as NoModuleError was being raised
#import time
#import asyncio


load_dotenv(find_dotenv())


class ServiceM8:

    ups = os.getenv('UPS_KEY')

    def __init__(self, data, servicem8_key):
        self.data = data
        self.servicem8_key = servicem8_key

    def create_job(self):
        """Extract json data & creates new job on ServiceM8.
        This function runs in parallel with the main program
        so checkout process speed is not affected."""

        # Check which key is being used
        plan = self.data['subscription']['plan_type']
        # Check which key is being used
        plan = self.data['subscription']['plan_type']  # Subscription Plan
        if self.servicem8_key == self.ups and plan == 'One-Off':
            # This ensures One-Off jobs are not created for main ServiceM8 account
            print('One-Off job not created for main ServiceM8 account')
            pass
        else:
            # Concatnate address
            address = self.data['customer']['address']['line1'] + ' ' + \
                self.data['customer']['address']['city'] + ' ' + \
                self.data['customer']['address']['state'] + ' ' + \
                self.data['customer']['address']['postal_code']
            plan = self.data['subscription']['plan_type']  # Subscription Plan

            # Custom_field/booking_details/selected_bins is a list of dicts
            # therefore 0 index is required to access the dict
            # then access the key 'dropdown' which is a dict and so forth
            # Using param custom field directly for ease of use
            bin_collection = self.data['booking_details'][0]['dropdown']['value']
            total_paid = self.data['subscription']['amount_paid']  # Total Amount
            # Convert cents to dollars & int to str
            total_paid = str(total_paid / 100)
            """Check plan type, if Bronze or Any Combo (One-Off),
            bin selection is passed to Servicem8 description"""
            plan = self.data['subscription']['plan_type']  # Subscription Plan
            if plan == 'Bronze Subscription' or plan == 'One-Off':
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

    def create_contact(self, job_uuid):
        """Extract json data & creates
        new job contact on ServiceM8."""

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


if __name__ == '__main__':
    ServiceM8()



# United Property ServiceM8 API Key: 'Basic cmV6ZW5kZS5mQG91dGxvb2suY29tOmQzNDQyZWY2LTk1MmUtNGI1Ny05Mzc0LTIwNTgxN2FhZjg2Yg=='


