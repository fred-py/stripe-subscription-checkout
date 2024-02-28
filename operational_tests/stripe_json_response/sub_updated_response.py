ja = {
    "object": {
        "id": "sub_1OXxZPL0FB5xAf6HiPiKcCWM",
        "object": "subscription",
        "application": None,
        "application_fee_percent": None,
        "automatic_tax": {
            "enabled": False,
            "liability": None
        },
        "billing_cycle_anchor": 1705484697,
        "billing_cycle_anchor_config": None,
        "billing_thresholds": None,
        "cancel_at": 1737107097,
        "cancel_at_period_end": True,
        "canceled_at": 1705828957,
        "cancellation_details": {
            "comment": None,
            "feedback": None,
            "reason": "cancellation_requested"
        },
        "collection_method": "charge_automatically",
        "created": 1705115259,
        "currency": "aud",
        "current_period_end": 1737107097,
        "current_period_start": 1705484697,
        "customer": "cus_PMgxdhXQvo5UKX",
        "days_until_due": None,
        "default_payment_method": "pm_1OXxZOL0FB5xAf6HRVi7GFSR",
        "default_source": None,
        "default_tax_rates": [
        ],
        "description": None,
        "discount": None,
        "ended_at": None,
        "invoice_settings": {
            "issuer": {
                "type": "self"
            }
        },
        "items": {
            "object": "list",
            "data": [
                {
                    "id": "si_PMgx0lmnNbO1AO",
                    "object": "subscription_item",
                    "billing_thresholds": None,
                    "created": 1705115260,
                    "metadata": {
                    },
                    "plan": {
                        "id": "price_1OUjokL0FB5xAf6HVVERJBI9",
                        "object": "plan",
                        "active": True,
                        "aggregate_usage": None,
                        "amount": 17900,
                        "amount_decimal": "17900",
                        "billing_scheme": "per_unit",
                        "created": 1704347410,
                        "currency": "aud",
                        "interval": "year",
                        "interval_count": 1,
                        "livemode": True,
                        "metadata": {
                        },
                        "nickname": None,
                        "product": "prod_PJMX57nA7ZIoLB",
                        "tiers_mode": None,
                        "transform_usage": None,
                        "trial_period_days": None,
                        "usage_type": "licensed"
                    },
                    "price": {
                        "id": "price_1OUjokL0FB5xAf6HVVERJBI9",
                        "object": "price",
                        "active": True,
                        "billing_scheme": "per_unit",
                        "created": 1704347410,
                        "currency": "aud",
                        "custom_unit_amount": None,
                        "livemode": True,
                        "lookup_key": None,
                        "metadata": {
                        },
                        "nickname": None,
                        "product": "prod_PJMX57nA7ZIoLB",
                        "recurring": {
                            "aggregate_usage": None,
                            "interval": "year",
                            "interval_count": 1,
                            "trial_period_days": None,
                            "usage_type": "licensed"
                        },
                        "tax_behavior": "unspecified",
                        "tiers_mode": None,
                        "transform_quantity": None,
                        "type": "recurring",
                        "unit_amount": 17900,
                        "unit_amount_decimal": "17900"
                    },
                    "quantity": 1,
                    "subscription": "sub_1OXxZPL0FB5xAf6HiPiKcCWM",
                    "tax_rates": [
                    ]
                }
            ],
            "has_more": False,
            "total_count": 1,
            "url": "/v1/subscription_items?subscription=sub_1OXxZPL0FB5xAf6HiPiKcCWM"
        },
        "latest_invoice": "in_1OZVg5L0FB5xAf6H85XeqweX",
        "livemode": True,
        "metadata": {
        },
        "next_pending_invoice_item_invoice": None,
        "on_behalf_of": None,
        "pause_collection": None,
        "payment_settings": {
            "payment_method_options": None,
            "payment_method_types": None,
            "save_default_payment_method": "off"
        },
        "pending_invoice_item_interval": None,
        "pending_setup_intent": None,
        "pending_update": None,
        "plan": {
            "id": "price_1OUjokL0FB5xAf6HVVERJBI9",
            "object": "plan",
            "active": True,
            "aggregate_usage": None,
            "amount": 17900,
            "amount_decimal": "17900",
            "billing_scheme": "per_unit",
            "created": 1704347410,
            "currency": "aud",
            "interval": "year",
            "interval_count": 1,
            "livemode": True,
            "metadata": {
            },
            "nickname": None,
            "product": "prod_PJMX57nA7ZIoLB",
            "tiers_mode": None,
            "transform_usage": None,
            "trial_period_days": None,
            "usage_type": "licensed"
        },
        "quantity": 1,
        "schedule": None,
        "start_date": 1705115259,
        "status": "active",
        "test_clock": None,
        "transfer_data": None,
        "trial_end": None,
        "trial_settings": {
            "end_behavior": {
                "missing_payment_method": "create_invoice"
            }
        },
        "trial_start": None
    },
    "previous_attributes": {
        "cancel_at": None,
        "cancel_at_period_end": False,
        "canceled_at": None,
        "cancellation_details": {
            "reason": None
        }
    }
}

plan = ja['object']['items']['data'][0]['plan']['amount']
cus = ja['object']['customer']
print(f'Customer: {cus} requested cancellation of plan valued at: {plan}')