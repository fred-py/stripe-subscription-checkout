import stripe
import json
import os
#import asyncio  # For asyncrounous tasks triggered by webhook
from flask import Flask, render_template, jsonify, request, send_from_directory, redirect
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


def check_id_create_checkout(price, domain_url):
    """Check Stripe Price Id and creates 
    checkout based on price conditions"""
    try:
        if price == os.getenv('ANY_COMBO_PRICE_ID'):
            checkout_session =stripe.checkout.Session.create(
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

# Set up for testing later on
if __name__ == '__main__':
    create_checkout()
