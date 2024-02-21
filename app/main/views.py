"""Holds routes for main blueprint
Stripe Checkout Routes"""

import stripe
import json
import os
from flask import render_template, redirect, url_for, abort, \
    flash, request, current_app, make_response, send_from_directory, jsonify
#from flask_login import login_required, current_user
#from flask_sqlalchemy import get_debug_queries
from . import main
from dotenv import load_dotenv, find_dotenv
#from ..db_operations.servicem8_operations.data_transfer import data_transfer as d
from ..db_operations.prepare_data import prepare_session_data, Customer
from ..db_operations.crud_operations import add_user
from ..db_operations.query_ops import CustomerQuery as cq  # get_cus_id, get_order_date, get_payment_intent 


load_dotenv(find_dotenv())

stripe.api_version = '2020-08-27'
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

port = int(os.environ.get('PORT', 4242))  # This is needed to deploy on fl0


@main.route('/', methods=['GET', 'OPTIONS'])
def get_example():
    # Passing favicon en var to render on deployment
    return render_template('stripe/index.html', favicon=os.getenv('FAVICON'))


@main.route('/config', methods=['GET', 'OPTIONS'])
def get_publishable_key():
    return jsonify({
        'publishableKey': os.getenv('STRIPE_PUBLISHABLE_KEY'),
        'comboPrice': os.getenv('ANY_COMBO_PRICE_ID'),
        'silverPrice': os.getenv('SILVER_PRICE_ID'),
        'goldPrice': os.getenv('GOLD_PRICE_ID'),
        'oneOff': os.getenv('ONE_OFF_PRICE_ID'),
    })


# Fetch the Checkout Session to display the JSON result on the success page
@main.route('/checkout-session', methods=['GET'])
def get_checkout_session():
    id = request.args.get('sessionId')
    checkout_session = stripe.checkout.Session.retrieve(id)
    return jsonify(checkout_session)


@main.route('/create-checkout-session', methods=['POST', 'OPTIONS'])
def create_checkout_session():  # Asynchronous function
    price = request.form.get('priceId')
    domain_url = os.getenv('DOMAIN')
    try:
        # Create new Checkout Session for the order
        # For full details see https://stripe.com/docs/api/checkout/sessions/create
        # Set adjustable quantity to only be enabled for the Broze & One-off price
        # No concise way of doing this as line_items only takes list of dicts
        # and once adjustable_quantity is included even if set to false,
        # it fails to return products with no adjustable quantity
        # Hence the creation of two checkout sessions
        if price == os.getenv('ANY_COMBO_PRICE_ID'):
            checkout_session = stripe.checkout.Session.create(
                #success_url=domain_url + '/success.html?session_id={CHECKOUT_SESSION_ID}',
                success_url='https://unitedpropertyservices.au/wheelie-wash-subscribed/?session_id={CHECKOUT_SESSION_ID}',
                # Neither return nor cancel URL works with embedded mode
                cancel_url=domain_url,  # + '/canceled.html',
                #return_url = 'https://unitedpropertyservices.au/wheelie-bin-clean/checkout/return?session_id={CHECKOUT_SESSION_ID}',
                mode='subscription',
                allow_promotion_codes=True,
                #discounts=[{
                #    'coupon': 'test_coupon',
                #}],
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
            )

        elif price == os.getenv('ONE_OFF_PRICE_ID'):
            checkout_session = stripe.checkout.Session.create(
                success_url='https://unitedpropertyservices.au/wheelie-wash-subscribed/?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url, # + '/canceled.html',
                mode='payment',
                customer_creation='always',  # Create a new customer if one is not provided. Only used in payment mode
                billing_address_collection='required',
                allow_promotion_codes=True,
                #discounts=[{
                #    'coupon': 'test_coupon',
                #}],
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
                allow_promotion_codes=True,
                #discounts=[{
                #    'coupon': 'test_coupon',
                #}],
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


@main.route('/customer-portal', methods=['POST'])
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


@main.route('/webhook', methods=['POST'])
def webhook_received():
    # You can use webhooks to receive information about asynchronous payment events.
    # For more about our webhook events check out https://stripe.com/docs/webhooks.
    # https://stripe.com/docs/payments/checkout/fulfill-orders#create-event-handler
    webhook_secret = os.getenv('STRIPE_WEBHOOK_SECRET')
    request_data = json.loads(request.data)

    if webhook_secret:
        # Retrieve the event by verifying the signature using 
        # the raw body and secret if webhook signing is configured.
        # Store a reference to this header value for later use
        signature = request.headers.get('stripe-signature')
        try:
            event = stripe.Webhook.construct_event(
                payload=request.data,
                sig_header=signature,
                secret=webhook_secret)
            data = event['data']
            event_type = event['type']   # Get the type of webhook event sent - used to check the status of PaymentIntents.
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
        
    # Get the type of webhook event sent - 
    # used to check the status of PaymentIntents.    
    else:
        data = request_data['data']
        event_type = request_data['type']
        data_object = data['object'] # Values added to metadata can be accessed from data_object - print(data_object)

    #print('event ' + event_type)

    uww = os.getenv('UWW_KEY')  # ServiceM8 Wheelie Wash Keys
    ups = os.getenv('UPS_KEY')  # ServiceM8 United Property Services Keys

    # NOTE: PaymentIntent is created automatically however it is not
    # automatically attached to cus_id\
    # Listen to PaymentIntent events, and use stripe.Customer.modify
    # To attached PaymentIntent customer metadata
    if event_type == 'payment_intent.created' and 'payment_intend.payment_failed':
        # Follow up abandoned carts
        print('Use this to follow up abandoned carts? add to the db under a new table?')

    elif event_type == 'payment_intent.succeeded':
        cus_id = data_object['customer']  # Get cus_id from data_object
        intent_id = data_object['id']  # Get PaymentIntent_id from data_object
        # https://stripe.com/docs/api/metadata
        # Attach payment intent id to customer metadata
        stripe.Customer.modify(
            cus_id,
            metadata={'paymentintent_id': intent_id}
        )

    elif event_type == 'invoice.paid':
        cus_id = data_object['customer']
        # Data Object contains json from any given event
        invoice_id = data_object['id']
        amount_paid = data_object['amount_paid']
        invoice_url = data_object['hosted_invoice_url']
        inv_description = data_object['lines']['data'][0]['description']
        # Add invoice information to customer metadata
        stripe.Customer.modify(
            cus_id,
            metadata={
                'invoice_id': invoice_id,
                'amount_paid': amount_paid,
                'invoice_url': invoice_url,
                'inv_description': inv_description,
            }
        )

    elif event_type == 'checkout.session.completed':
        session = stripe.checkout.Session.retrieve(
            event['data']['object']['id'],
            # Use expand to retrieve additional details from checkout session
            # Note that retrieving too many items will slow down response time
            # https://stripe.com/docs/api/expanding_objects
            # https://stripe.com/docs/expand
            expand=['customer', 'line_items', 'custom_fields'],
            )

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

            session_info = prepare_session_data(data)
            user = Customer(**session_info)  # Dataclass Unpacks Dict
            # Add customer to the database
            add_user(user)
            print(user.name)
            #add_customer(**)
            # Convert, combine and pass data to ServiceM8
            # Asyncio ensures the function runs in parallel with the main program
            # Start both tasks and gather their results
            #asyncio.create_task(create_job(data, uww))
            #asyncio.create_task(create_job(data, ups))
            
            #ww_acc = d.ServiceM8(data, uww)
            #uuid = ww_acc.create_job()
            #ww_acc.create_contact(uuid)
            """USE ASYNCIO AND MEASURE PERFORMANCE AND OUTPUT TIME SAVED
            TO GO ON DOCUMENTATION eg. x seconds faster y% improvement"""

            """NOTHING TO BE SENT TO UPS UNTIL FURTHER NOTICE"""
            #ups_acc = d.ServiceM8(data, ups)
            #uuid = ups_acc.create_job()  # Create job returns uuid
            #ups_acc.create_contact(uuid)
    # Handle the event
    elif event_type == 'customer.subscription.updated':
        subscription = event['data']['object']
        date_canceled = subscription.canceled_at  # Date cancelation was requested
        if date_canceled is None:
            print('Subscription is active')
            #pass
        else:
            # Response value from subscription.canceled_at
            # is in seconds, convert to datetime
            #date_canceled = int(subscription.canceled_at)  # Date cancelation was requested
            #date_cancel_at = int(subscription.cancel_at)  # Date cancelation will take effect
            #cancel_req = datetime.datetime.fromtimestamp(date_canceled)
            #cancel_at = datetime.datetime.fromtimestamp(date_cancel_at)
            plan = subscription['items']['data'][0]['plan']['amount']  
            cus_id = subscription['customer']
            



            # Cancel subscription 
            sub_id = subscription['id']
            stripe.Subscription.cancel(sub_id)

            # Process Refunds
            query = cq()  # Instatiate to create the application context
            p_intent_id = query.get_payment_intent(cus_id)  # Get intent_id from db needed for refund
            order_date = query.get_order_date(cus_id)  # Get order date from db needed for refund

            plan_id = subscription['items']['data'][0]['plan']['id']

            # Refund Logic - Check website for details!!!!!!!
            if plan_id == os.getenv('GOLD_PRICE_ID'):

                amount = 8000
            elif plan_id == os.getenv('SILVER_PRICE_ID'):
                amount = 5000
            elif plan_id == os.getenv('ANY_COMBO_PRICE_ID'):
                amount = 17900
            
            stripe.Refund.create(
                payment_intent=p_intent_id,
                amount=amount
            ) 



    elif event_type == 'subscription_schedule.canceled':
        subscription_schedule = event['data']['object']
        print(f'This is the OTHER THING: {subscription_schedule}')
    else:
        print('Unhandled event type {}'.format(event['type']))
    return jsonify({'status': 'success'})


@main.route('/app/<path:filename>')
def data_transfer(filename):
    """Serves any modules in app folder"""
    return send_from_directory(main.root_path + '/app/', filename)


if __name__ == '__main__':
    main.run(debug=True, port=port)