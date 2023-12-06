# https://developer.servicem8.com/reference/post-jobcontact-create
import json
import requests


def create_job(info, customer, custom_field):
    """Extract json data & creates new job on ServiceM8."""

    data = {'info': info, 'customer': customer, 'custom_filed': custom_field}
    # Concatnate address
    address = data['customer']['address']['line1'] + ' ' + \
        data['customer']['address']['city'] + ' ' + \
        data['customer']['address']['state'] + ' ' + \
        data['customer']['address']['postal_code']
    job_description = data['info'][1] # Job Description
    invoice_amount = data['info'][0] # Total Amount
    # bin_day = data['custom_field']['dropdown']['value'] # Bin Collection Day

    # Create new job
    url = "https://api.servicem8.com/api_1.0/job.json"

    payload = {
        "active": 1,
        "job_address": address,
        "geo_country": "Australia",
        "geo_state": "Western Australia",
        "status": "Quote",
        "job_description": job_description,
        "total_invoice_amount": invoice_amount,
        "invoice_sent": "yes",
        "payment_processed": "yes",
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": "Basic bWFya2V0aW5nQHVuaXRlZHByb3BlcnR5c2VydmljZXMuYXU6ODczZmMzMjgtNWM0YS00NjE4LTlmNWUtMjA4YjgyZTFjMzRi",
        "uuid": "x-record-uuid"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        print(response.text)
        job_uuid = response.headers['x-record-uuid']
        create_contact(job_uuid, data)

    except Exception as e:
        print(e)


def create_contact(job_uuid, data):
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
        "authorization": "Basic bWFya2V0aW5nQHVuaXRlZHByb3BlcnR5c2VydmljZXMuYXU6ODczZmMzMjgtNWM0YS00NjE4LTlmNWUtMjA4YjgyZTFjMzRi"
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        return f'create_contact: {response.text}'
    except Exception as e:
        print(e)


if __name__ == '__main__':
    create_job()










