"""Holds routes for main blueprint
Stripe Checkout Routes"""

import stripe
import logging
import json
import os
from flask import Flask, render_template, redirect, url_for, abort, \
    flash, request, current_app, session, make_response, send_from_directory, jsonify
import traceback
#from flask_login import login_required, current_user
#from flask_sqlalchemy import get_debug_queries
from . import main
from dotenv import load_dotenv, find_dotenv
from ..forms.interest_form import RegisterInterestForm, CommercialForm, ContactForm
from ..db_operations.servicem8_operations import data_transfer as d
from ..db_operations.prepare_data import prepare_session_data, Customer
from ..db_operations.crud_operations import add_user, add_lead, add_commercial, add_one_off_user, get_email
from ..models import Lead
#
# from ..db_operations.query_ops import CustomerQuery as cq  # get_cus_id, get_order_date, get_payment_intent 
from ..emails import send_email, send_error_email
from app.api.auth import token_auth
from ..decorators import basic_auth_required

load_dotenv(find_dotenv())

stripe.api_version = '2020-08-27'
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

ups = os.getenv('UPS_KEY')  # ServiceM8 United Property Services Keys


@main.route('/new', methods=['GET', 'POST', 'OPTIONS'])
def get_sub_page_new():
    form = RegisterInterestForm()

    if form.validate_on_submit():
        email = form.email.data
        lead = get_email(email)
        if lead is None:
            data = {
                'name': form.name.data,
                'email': form.email.data,
                'mobile': form.mobile.data,
                'street': form.street.data,
                'city': form.city.data,
                'postcode': form.postcode.data,
                'service': form.service.data,
            }
            # Saves to database
            # Returns lead object that is passed to 
            # name parameter on redirect to retrieve Lead name
            # This reduces database queries
            try:
                lead = add_lead(data, test=True)
            except Exception as e:
                raise f'An error occurred adding lead contact to database{e}'


            # Sends internal email notification
            sbj = 'Someone has registered their interest in Wheelie Wash'
            template = 'database/mail/user_interest'
            recipient1 = 'rezende.f@outlook.com'
            recipient2 = 'info@wheeliewash.au'
            recipient3 = 'marketing@unitedpropertyservices.au'
            
            # Unable to send email to a list of addresses - temporary solution below.
            send_email(recipient1, sbj, template, **data)
            send_email(recipient2, sbj, template, **data)
            send_email(recipient3, sbj, template, **data)
            flash('Thank you for registering your interest!', 'success')  # Add a success message 
            session['known'] = False
            name = lead.name  # Set name for success message



            # If AJAX Request, return JSON
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({
                    'success': True,
                    'message': f'Thank you for registering your interest, {name}!, We will be in touch as soon as our services expand to your area.',
                    'name': name
                })
            # Fallback for non-AJAX
            return render_template('stripe/index.html', form=form, favicon=os.getenv('FAVICON'))
     
        else:
            # If email exists
            session['known'] = True
            flash('Email address already in use', 'warning')  # Add a warning message 
      
            # If AJAX request, return JSON with flash message
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({
                    'success': False,
                    'message': 'Email address already in use'
                })
    return render_template('stripe/index_new.html', form=form, favicon=os.getenv('FAVICON'))



@main.route('/', methods=['GET', 'POST', 'OPTIONS'])
def get_sub_page():
    form = RegisterInterestForm()

    if form.validate_on_submit():
        email = form.email.data
        lead = get_email(email)
        if lead is None:
            data = {
                'name': form.name.data,
                'email': form.email.data,
                'mobile': form.mobile.data,
                'street': form.street.data,
                'city': form.city.data,
                'postcode': form.postcode.data,
                'service': form.service.data,
            }
            # Saves to database
            # Returns lead object that is passed to 
            # name parameter on redirect to retrieve Lead name
            # This reduces database queries
            try:
                lead = add_lead(data, test=True)
            except Exception as e:
                raise f'An error occurred adding lead contact to database{e}'


            # Sends internal email notification
            sbj = 'Someone has registered their interest in Wheelie Wash'
            template = 'database/mail/user_interest'
            recipient1 = 'rezende.f@outlook.com'
            recipient2 = 'info@wheeliewash.au'
            recipient3 = 'marketing@unitedpropertyservices.au'
            
            # Unable to send email to a list of addresses - temporary solution below.
            send_email(recipient1, sbj, template, **data)
            send_email(recipient2, sbj, template, **data)
            send_email(recipient3, sbj, template, **data)
            flash('Thank you for registering your interest!', 'success')  # Add a success message 
            session['known'] = False
            name = lead.name  # Set name for success message



            # If AJAX Request, return JSON
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({
                    'success': True,
                    'message': f'Thank you for registering your interest, {name}!, We will be in touch as soon as our services expand to your area.',
                    'name': name
                })
            # Fallback for non-AJAX
            return render_template('stripe/index.html', form=form, favicon=os.getenv('FAVICON'))
     
        else:
            # If email exists
            session['known'] = True
            flash('Email address already in use', 'warning')  # Add a warning message 
      
            # If AJAX request, return JSON with flash message
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({
                    'success': False,
                    'message': 'Email address already in use'
                })
    return render_template('stripe/index.html', form=form, favicon=os.getenv('FAVICON'))


@main.route('/contact-us', methods=['GET', 'POST'])
def contact_us():
    """
    """
    enquiry = request.form.get('priceId')
    if enquiry == 'commercial':
        form = CommercialForm()
    else:
        form = ContactForm()

    if form.validate_on_submit():

        email = form.email.data
        enquiry = request.form.get('priceId')
        lead = get_email(email, model=enquiry)
        if lead is None:
            data = {
                'subscription': False,
                'name': form.name.data,
                'email': form.email.data,
                'mobile': form.mobile.data,
                'street': form.street.data,
                'city': form.city.data,
                'postcode': form.postcode.data,
                'service': form.service.data,
                'message': form.message.data,
            }
            print(f'ONE OFF DATA STRUCTURE: ======> {data}')
            # Saves to database
            # Returns lead object that is passed to 
            # name parameter on redirect to retrieve Lead name
            # This reduces database queries
            try:
                if enquiry == 'commercial':
                    lead = add_commercial(data)
                else:
                    lead = add_one_off_user(data)
            except Exception as e:
                raise f'An error occurred adding one-off enquiry to database{e}'

            try:
                # Sends internal WheelieWashDBWheelieWashDBemail notification
                sbj = 'Someone has registered their interest in Wheelie Wash'
                template = 'database/mail/user_interest'
                recipient1 = 'rezende.f@outlook.com'
                recipient2 = 'info@wheeliewash.au'
                recipient3 = 'marketing@unitedpropertyservices.au'
                # Unable to send email to a list of addresses - temporary solution below.
                send_email(recipient1, sbj, template, **data)
                send_email(recipient2, sbj, template, **data)
                send_email(recipient3, sbj, template, **data)
            except Exception as e:
                raise f'An error occurred while sending one-off email notification: {e}'
            
            try:
                ups_acc = d.ServiceM8(data, ups)
                uuid = ups_acc.create_job()  # Create job returns uuid
                ups_acc.create_contact(uuid)
            except Exception:
                raise Exception('An error occurred adding user to ServiceM8')
            

            flash('Thank you for registering your interest!', 'success')  # Add a success message 
            session['known'] = False
            name = lead.name  # Set name for success message


            # If AJAX Request, return JSON
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({
                    'success': True,
                    'message': f'Thank you for reaching out, {name}!, We will be in touch shortly.',
                    'name': name
                })
            # Fallback for non-AJAX
            return render_template(
                'stripe/contact.html',
                form=form,
                enquiry=enquiry,  # Pass to Jinja
                favicon=os.getenv('FAVICON'))

        else:
            # If email exists
            session['known'] = True
            flash('Email address already in use', 'warning')  # Add a warning message 

            # If AJAX request, return JSON with flash message
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({
                    'success': False,
                    'message': 'Email address already in use'
                })
    return render_template(
        'stripe/contact.html',
        enquiry=enquiry,
        form=form,
        favicon=os.getenv('FAVICON'))


@main.route('/bootstrap', methods=['GET', 'OPTIONS'])
def get_bootstrap_test():
    # Passing favicon en var to render on deployment
    return render_template('stripe/index_bootstrap.html', favicon=os.getenv('FAVICON'))


@main.route('/config', methods=['GET', 'OPTIONS'])
def get_publishable_key():
    """
    Receives priceId from <form> <input>

    Returns stripe product publishable
    key value from environment variable

    args: str - priceId eg. oneOff, silverPrice
    """
    return jsonify({
        'publishableKey': os.getenv('STRIPE_PUBLISHABLE_KEY'),

        'oneBin2weeks': os.getenv('ONE_BIN_2_WEEKS'),
        'oneBin4weeks': os.getenv('ONE_BIN_4_WEEKS'),
        'oneBin8weeks': os.getenv('ONE_BIN_8_WEEKS'),
        'oneBinOneOff': os.getenv('ONE_BIN_ONE_OFF'),

        'twoBins2weeks': os.getenv('TWO_BINS_2_WEEKS'),
        'twoBins4weeks': os.getenv('TWO_BINS_4_WEEKS'),
        'twoBins8weeks': os.getenv('TWO_BINS_8_WEEKS'),
        'twoBinsOneOff': os.getenv('TWO_BINS_ONE_OFF'),

        'threeBins2weeks': os.getenv('THREE_BINS_2_WEEKS'),
        'threeBins4weeks': os.getenv('THREE_BINS_4_WEEKS'),
        'threeBins8weeks': os.getenv('THREE_BINS_8_WEEKS'),
        'threeBinsOneOff': os.getenv('THREE_BINS_ONE_OFF'),

        'comboPrice': os.getenv('ANY_COMBO_PRICE_ID'),
        'silverPrice': os.getenv('SILVER_PRICE_ID'),
        'goldPrice': os.getenv('GOLD_PRICE_ID'),
    })


# Fetch the Checkout Session to display the JSON result on the success page
@main.route('/checkout-session', methods=['GET'])
def get_checkout_session():
    id = request.args.get('sessionId')
    checkout_session = stripe.checkout.Session.retrieve(id)
    return jsonify(checkout_session)


@main.route('/create-checkout-session', methods=['POST', 'OPTIONS'])
def create_checkout_session():
    price = request.form.get('priceId')
    logging.info(f"Received priceId: {price}, User-Agent: {request.headers.get('User-Agent')}")
    #if not price:
    #    logging.error("priceId is empty or missing")
    #   return jsonify({'error': {'message': 'Missing priceId'}}), 400
    domain_url = os.getenv('DOMAIN')  # Domain if fetched by back arrow icon on stripe hoted
    try:
        # Create new Checkout Session for the order
        # For full details see https://stripe.com/docs/api/checkout/sessions/create
        # Set adjustable quantity to only be enabled for the Broze & One-off price
        # No concise way of doing this as line_items only takes list of dicts
        # and once adjustable_quantity is included even if set to false,
        # it fails to return products with no adjustable quantity
        # Hence the creation of two checkout sessions
        oo_1 = os.getenv('ONE_BIN_ONE_OFF')
        oo_2 = os.getenv('TWO_BINS_ONE_OFF')
        oo_3 = os.getenv('THREE_BINS_ONE_OFF')
        one_offs = [oo_1, oo_2, oo_3]

        
        if price not in one_offs:
            checkout_session = stripe.checkout.Session.create(
                
                success_url='https://unitedpropertyservices.au/wheelie-wash-subscribed/?session_id={CHECKOUT_SESSION_ID}',
                # Neither return nor cancel URL works with embedded mode
                cancel_url=domain_url,
                mode='subscription',
                allow_promotion_codes=True,
                #discounts=[{
                #    'coupon': 'test_coupon',
                #}],
                billing_address_collection='required',
                line_items=[{
                    'price': price,
                    'adjustable_quantity':
                        # Ensure max is has the save value on stripe dashboard
                        {'enabled': False},
                    'quantity': 1
                }],
                phone_number_collection={'enabled': True},
                custom_fields=[
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
                                {'label': 'All 3 bins', 'value': 'All'},
                            ]
                        }
                    },
                ],
            )
        elif price in one_offs:
            checkout_session = stripe.checkout.Session.create(
                
                success_url='https://unitedpropertyservices.au/wheelie-wash-subscribed/?session_id={CHECKOUT_SESSION_ID}',
                # Neither return nor cancel URL works with embedded mode
                cancel_url=domain_url,
                mode='payment',
                allow_promotion_codes=True,
                #discounts=[{
                #    'coupon': 'test_coupon',
                #}],
                billing_address_collection='required',
                phone_number_collection={'enabled': True},
                custom_fields=[
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
                                {'label': 'All 3 bins', 'value': 'All'},
                            ]
                        }
                    },
                ],
            )

        else:
            # Loads both Gold and Silver price
            checkout_session = stripe.checkout.Session.create(
                success_url='https://unitedpropertyservices.au/wheelie-wash-subscribed/?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url,  # + '/canceled.html',
                mode='subscription',
                billing_address_collection='required',
                allow_promotion_codes=True,
                #discounts=[{
                #    'coupon': 'test_coupon',
                #}],
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
                        'key': 'confirm_service_area',
                        'optional': False,    
                        'label': {'type': 'custom', 'custom': 'Have you confirmed we service your area?'},
                        'type': 'dropdown',
                        'dropdown': {
                            'options': [
                                {'label': 'Yes, I have checked that my street is within the serviced area', 'value': 'yes'},
                                {'label': 'No, I have not checked the map. Check map before proceeding', 'value': 'no'},
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
        logging.error(f"Stripe error: {str(e)}")
        return render_template('errors/400.html')


@main.route('/error_test')
def test_error():
    return render_template('errors/400.html')

@main.route('/customer-portal', methods=['POST'])
def customer_portal():
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
            traceback_str = traceback.format_exc()
            return jsonify(status=500, content=f'Unexpected error: {e}\n{traceback_str}')

    # Get the type of webhook event sent - 
    # used to check the status of PaymentIntents.    
    else:
        data = request_data['data']
        event_type = request_data['type']
        data_object = data['object'] # Values added to metadata can be accessed from data_object - print(data_object)
        event = request_data

    #print('event ' + event_type)
    # NOTE: PaymentIntent is created automatically however it is not
    # automatically attached to cus_id\
    # Listen to PaymentIntent events, and use stripe.Customer.modify
    # To attached PaymentIntent customer metadata
    if event_type == 'payment_intend.payment_failed':
        # Follow up abandoned carts
        # add to the db under a new table? or send email?
        pass
    
    elif event_type == 'invoice.paid':
        
        cus_id = data_object['customer']
        # Data Object contains json from any given event
        invoice_id = data_object['id']
        amount_paid = data_object['amount_paid']
        invoice_url = data_object['hosted_invoice_url']
        inv_description = data_object['lines']['data'][0]['description']
        pi_id = data_object.get('payment_intent')


        # Add invoice information to customer metadata
        stripe.Customer.modify(
            cus_id,
            metadata={
                'invoice_id': invoice_id,
                'amount_paid': amount_paid,
                'invoice_url': invoice_url,
                'inv_description': inv_description,
                'payment_intent': pi_id
            }
        )
       #return cus_obj
        #print(f'****** Customer Updated *invoice.paid* METADATA: {cus_obj}')

    elif event_type == 'checkout.session.completed':
        
        #cus_id = data_object['customer']
        # Data Object contains json from any given event
        #pi_id = data_object.get('payment_intent')

        # Add invoice information to customer metadata
        #stripe.Customer.modify(
        #    cus_id,
        #    metadata={
        #        'payment_intent': pi_id
        #    }
        #)
        
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

            data = {
                    'customer': customer,
                    'subscription': {
                        'amount_paid': info[0],
                        'plan_type': info[1],
                    },
                    'booking_details': custom_field,
            }

            try:
                ups_acc = d.ServiceM8(data, ups)
                uuid = ups_acc.create_job()  # Create job returns uuid
                ups_acc.create_contact(uuid)
            except Exception as e:
                raise f'An error occurred adding user to ServiceM8{e}'

            session_info = prepare_session_data(data)
            try:
                user = Customer(**session_info)  # Dataclass Unpacks Dict
                # Add customer to the database
                add_user(user)
            except Exception as e:
                raise f'An error occurred adding user to database{e}'
            #print(user.name)
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
    # Handle the event
    elif event_type == 'customer.subscription.updated':
        subscription = event['data']['object']
        date_canceled = subscription.canceled_at  # Date cancelation was requested
        if date_canceled is None:
            #print('Subscription is active')
            pass
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
        print(f'subscription schedule: {subscription_schedule}')
    else:
        print('Unhandled event type {}'.format(event['type']))
    return jsonify({'status': 'success'})


@main.route('/app/<path:filename>')
def data_transfer(filename):
    """Serves any modules in app folder"""
    return send_from_directory(main.root_path + '/app/', filename)


@main.route('/robots.txt')
def robots():
    """Servers robots file for website indexing/SEO"""
    return send_from_directory(current_app.static_folder, 'robots.txt')


if __name__ == '__main__':
    main.run()