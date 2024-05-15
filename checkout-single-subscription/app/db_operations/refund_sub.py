import os
from datetime import datetime, timedelta
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


def calculate_refund(days_lapsed, plan_id):
    """Calculate the refund amount
    based on the plan and order date."""

    if plan_id == os.getenv('GOLD_PRICE_ID') and days_lapsed < 182:
        amount = 10800  # 50% of the Gold plan
    elif plan_id == os.getenv('GOLD_PRICE_ID') and days_lapsed > 182:
        amount = 10800  # 100% of the Gold plan
    elif plan_id == os.getenv('SILVER_PRICE_ID'):
        amount = 5000
    elif plan_id == os.getenv('ANY_COMBO_PRICE_ID'):
        amount = 17900
    return amount


def time_lapsed(order_date):
    """Calculate the time lapsed since the order date."""
    date = order_date
    time_lapsed = datetime.now() - date
    print(time_lapsed)
    return time_lapsed


order_date = '2023-02-13 14:43:09.247839'
# .strftime converts string to datetime object
date = datetime.strptime(order_date, '%Y-%m-%d %H:%M:%S.%f')


time_lapsed(date)
days_lapsed = time_lapsed(date).days  # Extract the days from the timedelta object

if days_lapsed > 182:
    print('Refund x')
else:
    print('Refund 50% of the total amount')

weekday = datetime.weekday(date)
print(weekday)

"""Workout Clean Cycle Start Date"""
# set start date based on intergers to match datetime.weekday()
# Eg. Monday = 0, Tuesday = 1, Wednesday = 2, Thursday = 3, Friday = 4, Saturday = 5, Sunday = 6
# Get the weekday of the order date to then set the exact
# start date of the clean cycle
# somehow get the start date of the clean cycle

start_date = 'wednesday'
