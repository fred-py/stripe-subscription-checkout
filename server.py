#! /usr/bin/env python3.8

"""
server.py
Stripe Sample.
Python 3.6 or newer required.
"""

import stripe
import json
import os
import asyncio  # For asyncrounous tasks triggered by webhook
from flask import Flask, render_template, jsonify, request, send_from_directory, redirect
from flask_cors import CORS
from dotenv import load_dotenv, find_dotenv
from server.data import create_job
import time



# Setup Stripe python client library
load_dotenv(find_dotenv())
# For sample support and debugging, not required for production:
stripe.set_app_info(
    'stripe-samples/checkout-single-subscription',
    version='0.0.1',
    url='https://github.com/stripe-samples/checkout-single-subscription')

stripe.api_version = '2020-08-27'
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

#static_dir = str(os.path.abspath(os.path.join(
#    __file__, '..', os.getenv('STATIC_DIR'))))

#app = Flask(__name__, static_folder=static_dir,
#            static_url_path=', template_folder=static_dir)

app = Flask(
    __name__,
    static_folder='client',
    static_url_path='',
    template_folder='client',
)

CORS(app, origins=['https://unitedpropertyservices.au/',])


"""@app.after_request
def add_cors_headers(response):
    response.headers.add('Access-Control-Allow-Origin', 'https://unitedpropertyservices.au/')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response"""


port = int(os.environ.get('PORT', 4242))  # This is needed to deploy on fl0


@app.route('/', methods=['GET', 'OPTIONS'])
def get_example():
    # Passing favicon en var to render on deployment
    return render_template('index_stacked.html', favicon=os.getenv('FAVICON'))


@app.route('/config', methods=['GET', 'OPTIONS'])
def get_publishable_key():
    return jsonify({
        'publishableKey': os.getenv('STRIPE_PUBLISHABLE_KEY'),
        'comboPrice': os.getenv('ANY_COMBO_PRICE_ID'),
        'silverPrice': os.getenv('SILVER_PRICE_ID'),
        'goldPrice': os.getenv('GOLD_PRICE_ID'),
        'oneOff': os.getenv('ONE_OFF_PRICE_ID'),
    })


# Fetch the Checkout Session to display the JSON result on the success page
@app.route('/checkout-session', methods=['GET'])
def get_checkout_session():
    id = request.args.get('sessionId')
    checkout_session = stripe.checkout.Session.retrieve(id)
    return jsonify(checkout_session)


@app.route('/create-checkout-session', methods=['POST', 'OPTIONS'])
async def create_checkout_session():  # Asynchronous function
    price = request.form.get('priceId')
    domain_url = os.getenv('DOMAIN')

    try:
        # Create new Checkout Session for the order
        # Other optional params include:
        # [billing_address_collection] - to display billing address details on the page
        # [customer] - if you have an existing Stripe Customer ID
        # [customer_email] - lets you prefill the email input in the form
        # [automatic_tax] - to automatically calculate sales tax, VAT and GST in the checkout page
        # For full details see https://stripe.com/docs/api/checkout/sessions/create

        # Set adjustable quantity to only be enabled to the combo price
        # No concise manner of doing this as line_items only takes list of dicts
        # and once adjustable_quantity is included even if set to false,
        # it fails to return products with no adjustable quantity
        # Hence the creation of two checkout sessions
        if price == os.getenv('ANY_COMBO_PRICE_ID'):
            # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
            
            checkout_session = stripe.checkout.Session.create(
                #success_url=domain_url + '/success.html?session_id={CHECKOUT_SESSION_ID}',
                success_url='https://unitedpropertyservices.au/wheelie-wash-subscribed/?session_id={CHECKOUT_SESSION_ID}',
                # Neither return nor cancel URL works with embedded mode
                cancel_url=domain_url,  # + '/canceled.html',
                #return_url = 'https://unitedpropertyservices.au/wheelie-bin-clean/checkout/return?session_id={CHECKOUT_SESSION_ID}',
                mode='subscription',
                billing_address_collection='required',
                # automatic_tax={'enabled': True},
                line_items=[{
                    'price': price,
                    'adjustable_quantity':
                        # Ensure max is has the save value on stripe dashboard
                        {'enabled': True, 'minimum': 1, 'maximum': 3},
                    'quantity': 1
                }],
                phone_number_collection={'enabled': True},
                custom_fields=[
                    {
                        'key': 'collection_date',
                        'label': {'type': 'custom', 'custom': 'Bin Collection Day'},
                        'type': 'dropdown',
                        'dropdown': {
                            'options': [
                                {'label': 'Monday', 'value': 'monday'},
                                {'label': 'Tuesday', 'value': 'tuesday'},
                                {'label': 'Wednesday', 'value': 'wednesday'},
                                {'label': 'Thursday', 'value': 'thursday'},
                                {'label': 'Friday', 'value': 'friday'},
                            ],
                        },
                    },

                    {
                        'key': 'select_bins',
                        'label': {'type': 'custom', 'custom': 'Select the bin(s)to be cleaned.'},
                        'type': 'dropdown',
                        'dropdown': {
                            'options': [
                                {'label': 'Red bin', 'value': 'R'},
                                {'label': 'Yellow bin', 'value': 'Y'},
                                {'label': 'Green bin', 'value': 'G'},
                                {'label': 'Red and Green bins', 'value': 'RG'},
                                {'label': 'Red and Yellow bins', 'value': 'RY'},
                                {'label': 'Yellow and Green bins', 'value': 'YG'},
                                {'label': 'All bins', 'value': 'All'},
                            ]
                        }
                    }
                ],
                custom_text={
                    'submit': {'message': 'NOTE: Currently we only service the Margaret River region.'},
                },
                #return_url=domain_url + '/checkout/return?session_id={CHECKOUT_SESSION_ID}',
                #return_url='http://localhost:4242/checkout/return?session_id={CHECKOUT_SESSION_ID}',
            )

        elif price == os.getenv('ONE_OFF_PRICE_ID'):
            
            checkout_session = stripe.checkout.Session.create(
                success_url='https://unitedpropertyservices.au/wheelie-wash-subscribed/?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url, # + '/canceled.html',
                mode='payment',
                customer_creation='always',  # Create a new customer if one is not provided. Only used in payment mode
                billing_address_collection='required',

                line_items=[{
                    'price': price,
                    'adjustable_quantity':
                        # Ensure max is has the save value on stripe dashboard
                        {'enabled': True, 'minimum': 1, 'maximum': 3},
                    'quantity': 1
                }],
                phone_number_collection={'enabled': True},
                custom_fields=[
                    {
                        'key': 'tentative-day',
                        'label': {'type': 'custom', 'custom': 'When would you like your bin(s) cleaned?'},
                        'type': 'dropdown',
                        'dropdown': {
                            'options': [
                                {'label': 'Monday', 'value': 'monday'},
                                {'label': 'Tuesday', 'value': 'tuesday'},
                                {'label': 'Wednesday', 'value': 'wednesday'},
                                {'label': 'Thursday', 'value': 'thursday'},
                                {'label': 'Friday', 'value': 'friday'},
                            ],
                        },
                    },

                    {
                        'key': 'select_bins',
                        'label': {'type': 'custom', 'custom': 'Select the bin(s) to be cleaned.'},
                        'type': 'dropdown',
                        'dropdown': {
                            'options': [
                                {'label': 'Red bin', 'value': 'R'},
                                {'label': 'Yellow bin', 'value': 'Y'},
                                {'label': 'Green bin', 'value': 'G'},
                                {'label': 'Red and Green bins', 'value': 'RG'},
                                {'label': 'Red and Yellow bins', 'value': 'RY'},
                                {'label': 'Yellow and Green bins', 'value': 'YG'},
                                {'label': 'All bins', 'value': 'All'},
                            ]
                        }
                    }
                ],
                custom_text={
                    'submit': {'message': 'NOTE: We will get in touch to confirm a date.'}
                },

            )

        else:

            checkout_session = stripe.checkout.Session.create(
                success_url='https://unitedpropertyservices.au/wheelie-wash-subscribed/?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url,  # + '/canceled.html',
                mode='subscription',
                billing_address_collection='required',
                # automatic_tax={'enabled': True},
                line_items=[{
                    'price': price,
                    'quantity': 1
                }],
                phone_number_collection={'enabled': True},
                custom_fields=[
                    {
                        'key': 'collection_date',
                        'label': {'type': 'custom', 'custom': 'Bin Collection Day'},
                        'type': 'dropdown',
                        'dropdown': {
                            'options': [
                                {'label': 'Monday', 'value': 'monday'},
                                {'label': 'Tuesday', 'value': 'tuesday'},
                                {'label': 'Wednesday', 'value': 'wednesday'},
                                {'label': 'Thursday', 'value': 'thursday'},
                                {'label': 'Friday', 'value': 'friday'},
                            ],
                        },
                    },

                ],
                custom_text={
                    'submit': {'message': 'NOTE: Currently we only service the Margaret River region.'}
                },
            )
        return redirect(checkout_session.url, code=303)
    except Exception as e:
        return jsonify({'error': {'message': str(e)}}), 400



@app.route('/customer-portal', methods=['POST'])
def customer_portal():
    # For demonstration purposes, we're using the Checkout session to retrieve the customer ID.
    # Typically this is stored alongside the authenticated user in your database.
    checkout_session_id = request.form.get('sessionId')
    checkout_session = stripe.checkout.Session.retrieve(checkout_session_id)

    # This is the URL to which the customer will be redirected after they are
    # done managing their billing with the portal.
    return_url = os.getenv('CUSTOMER_PORTAL')

    session = stripe.billing_portal.Session.create(
        customer=checkout_session.customer,
        return_url=return_url,
    )
    return redirect(session.url, code=303)


@app.route('/webhook', methods=['POST'])
async def webhook_received():
    # You can use webhooks to receive information about asynchronous payment events.
    # For more about our webhook events check out https://stripe.com/docs/webhooks.
    # https://stripe.com/docs/payments/checkout/fulfill-orders#create-event-handler
    webhook_secret = os.getenv('STRIPE_WEBHOOK_SECRET')
    request_data = json.loads(request.data)

    if webhook_secret:
        # Retrieve the event by verifying the signature using the raw body and secret if webhook signing is configured.
        signature = request.headers.get('stripe-signature')
        try:
            event = stripe.Webhook.construct_event(
                payload=request.data,
                sig_header=signature,
                secret=webhook_secret)
            data = event['data']
            event_type = event['type']
            data_object = data['object']
        except ValueError as e:
            # Invalid payload
            return jsonify(status=400, content=f'Invalid payload: {e}')
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            return jsonify(status=400, content=f'Invalid signature: {e}')
        except Exception as e:
            # Catch unexpected errors
            return jsonify(status=500, content=f'Unexpected error: {e}')
        
    # Get the type of webhook event sent - used to check the status of PaymentIntents.    
    else:
        data = request_data['data']
        event_type = request_data['type']
        data_object = data['object']

    print('event ' + event_type)

    # Handle the checkout.session.completed event | Fulfill Order
    if event_type == 'checkout.session.completed':
        """Needs to return additional data"""
        session = stripe.checkout.Session.retrieve(
            event['data']['object']['id'],
            # Use expand to retrieve additional details from checkout session
            # Note that retrieving too many items will slow down response time
            expand=['customer', 'line_items', 'custom_fields'],  # https://stripe.com/docs/api/expanding_objects
            )                                   # https://stripe.com/docs/expand

        line_items = session.line_items
        for line_items in line_items.data:
            info = line_items.amount_total, line_items.description

            customer = session.customer
            custom_field = session.custom_fields

            # Create data object to pass to ServiceM8
            data = {
                    'customer': customer,
                    'subscription': {
                        'amount_paid': info[0],
                        'plan_type': info[1],
                    },
                    'booking_details': custom_field,
                }
            

            uww = os.getenv('UWW_KEY')  # ServiceM8 Wheelie Wash Keys

            ups = os.getenv('UPS_KEY')  # ServiceM8 United Property Services Keys
            # Convert, combine and pass data to ServiceM8
            # Asyncio ensures the function runs in parallel with the main program
            # Start both tasks and gather their results
            asyncio.create_task(create_job(data, uww))
            asyncio.create_task(create_job(data, ups))

        # Fulfill Order - Send to servicem8/database <=======*********
    return jsonify({'status': 'success'})


if __name__ == '__main__':
    app.run(debug=True, port=port)