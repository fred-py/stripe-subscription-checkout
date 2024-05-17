"""Selenium Indexed Documentation""" 
# https://selenium-python.readthedocs.io/
# https://www.browserstack.com/docs/automate/selenium/firefox-profile#python

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options  # Set up the drive to handle downloads.
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.select import Select  # For dropdown menus
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from street_names import addresses
# Testing
import random
from faker import Faker
import time as sleep


#options = Options()  # Create a new options folder
#options.add_argument("--headless")  # Run headless
options = FirefoxOptions()
options.set_preference('browser.helperApps.awaysAsk.force', False)
options.set_preference('formfill.autocomplete.search', False)
options.set_preference('browser.formfill.enableAutoFillSave', False)
options.set_preference("browser.formfill.enable", False)
#options.add_argument("--headless")  # Run headless


"""CHECKOUT TEST RUN WITH FAKE DETAILS"""
# Create an instance of Faker with Australian locale
faker = Faker('en_AU')

# Generate 10 random email addresses
email_list = [faker.email() for _ in range(600)]
# Create a dictionary with random email addresses as keys
email_dict = {email: None for email in email_list}
name_list = [faker.name() for _ in range(600)]


def create_mobile():
    """Generates a random australian mobile number"""
    number_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    ran = random.choice(number_list) + \
        random.choice(number_list) + \
        random.choice(number_list) + \
        random.choice(number_list)
    mobile = '04' + ran + ran
    return mobile


def random_weekday():
    """Selects a random weekday from a list, once
    dropdown menu is visible on checkcout page"""
    weekdays = ['m', 'tu', 'w', 't', 'f']
    day = random.choice(weekdays)
    return day


def random_bin_selection():
    """Selects a random bin, once
    dropdown menu is visible on checkout page"""
    bins = ['r', 'g', 'y', 'b', 'a']
    bin = random.choice(bins)
    return bin


post_code_options = ['6284', '6285', '6286', '6288', '6290']
suburb_options = ['Margaret River', 'Cowaramup', 'Witchcliffe', 'Redgate', 'Boranup']

mobile = create_mobile()
random_name = random.choice(name_list)
email_address = random.choice(email_list)
bin_collection = random_weekday()
success_card = '4242 4242 4242 4242'
expiry = '12/28'
cvc = '333'
street = random.choice(addresses)
suburb = random.choice(suburb_options)
postcode = random.choice(post_code_options)
bin = random_bin_selection()

local = 'http://localhost:5001/'
public = 'https://wheeliewash.2.sg-1.fl0.io/'


class Checkout:
    def __init__(self, driver, url, plan):
        self.driver = driver
        self.url = url
        self.plan = plan
    
class ChoosePlan(Checkout):
    def __init__(self, driver, url, plan):
        super().__init__(driver, url, plan)
    
    def load_url(self):
        try:
            self.driver.get(self.url)
        except WebDriverException as e:
            raise f"Error Accessing the URL {e} , the script will run again in 4 minutes"
    
    def select_plan(self):
        if self.plan == 'gold':
            btn = '#gold-plan-btn'
        elif self.plan == 'silver':
            btn = '#silver-plan-btn'
        elif self.plan == 'bronze':
            btn = '#combo-plan-btn'
        else:
            btn = '#one-off-btn'
            return btn
    
        try:
            button = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, btn))
            )
            button.click()
        except WebDriverException as e:
            raise f'select_plan: {e}'

class CustomerDetails(Checkout):
    def __init__(self, driver, plan):
        super().__init__(driver, plan)

    def enter_email(self):
        try:
            email = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#email'))
            )
            email.click()
            email.send_keys(email_address)
        except WebDriverException as e:
            raise f'enter_email: {e}'

    def enter_mobile(self):
        try:
            phone = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#phoneNumber'))
            )
            phone.click()
            phone.send_keys(mobile)
        except WebDriverException as e:
            raise f'enter_mobile: {e}'

    def bin_collection_day(self):
        try:
            # Use keyboard keys to navigate to bin collection dropdown menu
            # random_weekday() function selects a random weekday
            ActionChains(self.driver)\
                .key_down(Keys.TAB)\
                .key_up(Keys.TAB)\
                .key_down(Keys.ARROW_DOWN)\
                .send_keys(bin_collection)\
                .key_down(Keys.ENTER)\
                .key_up(Keys.ENTER)\
                .perform()
        except WebDriverException as e:
            raise f'bin_collection_day: {e}'
        
    def select_bin(self):
        if self.plan == 'bronze' or self.plan == 'one-off':
            try:
                ActionChains(self.driver)\
                    .key_down(Keys.TAB)\
                    .key_up(Keys.TAB)\
                    .key_down(Keys.ARROW_DOWN)\
                    .send_keys(bin)\
                    .key_down(Keys.ENTER)\
                    .key_up(Keys.ENTER)\
                    .perform()
            except WebDriverException as e:
                raise f'select_bin: {e}'
        else:
            pass
    
    def enter_card_number(self):
        try:
            card = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#cardNumber'))
            )
            card.click()
            card.send_keys(success_card)
        except WebDriverException as e:
            raise f'enter_card_number: {e}'

    def enter_expiry_date(self):
        try:
            expiry_date = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#cardExpiry'))
            )
            expiry_date.click()
            expiry_date.send_keys(expiry)
        except WebDriverException as e:
            raise f'enter_expiry_date: {e}'

    def enter_cvc_number(self):
        try:
            cvc_number = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#cardCvc'))
            )
            cvc_number.click()
            cvc_number.send_keys(cvc)
        except WebDriverException as e:
            raise f'enter_cvc_number: {e}'

    def enter_card_name(self):
        try:
            card_name = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#billingName'))
            )
            card_name.click()
            card_name.send_keys(random_name)
        except WebDriverException as e:
            raise f'enter_card_name: {e}'
        
    def enter_street_address(self):
        try:
            street_address = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#billingAddressLine1'))
            )
            street_address.click()
            street_address.send_keys(street)
        except WebDriverException as e:
            raise f'enter_street_address: {e}'

    def enter_suburb(self):
        try:
            # Use keyboard keys to navigate address details
            # The auto-complete feature gets in the way
            # This can be resolved by using the TAB key
            ActionChains(self.driver)\
                .key_down(Keys.ENTER)\
                .key_up(Keys.ENTER)\
                .perform()
                #.key_down(Keys.TAB)\
                #.key_up(Keys.TAB)\
        except WebDriverException as e:
            print(f'enter_suburb - Dropdown: {e}')
         
        try: 
            suburb_name = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#billingLocality'))
            )
            suburb_name.click()
            suburb_name.send_keys(suburb)
        except WebDriverException as e:
            print(f'enter_suburb: {e}')

            try:
                # Use keyboard keys to navigate address details
                # The auto-complete feature gets in the way
                # This can be resolved by using the TAB key
                ActionChains(self.driver)\
                    .key_down(Keys.ENTER)\
                    .key_up(Keys.ENTER)\
                    .perform()
                    #.key_down(Keys.TAB)\
                    #.key_up(Keys.TAB)\
            except WebDriverException as e:
                print(f'enter_suburb - Dropdown: {e}')
            
            try: 
                suburb_name = WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '#billingLocality'))
                )
                suburb_name.click()
                suburb_name.send_keys(suburb)
            except WebDriverException as e:
                print(f'enter_suburb: {e}')
        

    def enter_state(self):
        try:
            # Use keyboard keys to navigate to State dropdown menu
            # Selects w for WA
            ActionChains(self.driver)\
                .key_down(Keys.TAB)\
                .key_up(Keys.TAB)\
                .key_down(Keys.ARROW_DOWN)\
                .send_keys('w')\
                .key_down(Keys.ENTER)\
                .key_up(Keys.ENTER)\
                .perform()
        except WebDriverException as e:
            raise f'enter_state Selecting w: {e}'

        try:
            ActionChains(self.driver)\
                .key_down(Keys.ENTER)\
                .key_up(Keys.ENTER)\
                .perform()
        except WebDriverException as e:
            raise f'enter_state - Enter to exit pop-up: {e}'

    def enter_postcode(self):
        try:
            post_code = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#billingPostalCode'))
            )
            post_code.click()
            post_code.send_keys(postcode)
        except WebDriverException as e:
            raise f'enter_postcode: {e}'
        
        try:
            ActionChains(self.driver)\
                .key_down(Keys.ENTER)\
                .key_up(Keys.ENTER)\
                .perform()
        except WebDriverException as e:
            raise f'enter_postcode - Pressing Enter: {e}'
    
    def subscribe(self):
        try:
            subscribe = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'SubmitButton SubmitButton--incomplete'))
            )
            subscribe.click()
            WebDriverWait(self.driver, 20).until(EC.url_contains("unitedpropertyservices.au/wheelie-wash-subscribed/?session_id"))

        except WebDriverException as e:
            raise f'subscribe: {e}'

class RandomItems(Checkout):
    def __init__(self, driver):
        super().__init__(driver)




def checkout_test(plan, url):

    if plan == 'gold':
        btn = '#gold-plan-btn'
    elif plan == 'silver':
        btn = '#silver-plan-btn'
    elif plan == 'bronze':
        btn = '#combo-plan-btn'
    else:
        btn = '#one-off-btn'

    driver = webdriver.Firefox(options=options) # Create a WebDriver instance with FirefoxDriver and the custom options
    try:
        #driver.get("https://wheeliewash.2.sg-1.fl0.io")
        driver.get(url)
    except WebDriverException as e:
        raise Exception(f'driver.get error {e}')

    try:

        select_plan = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, btn))
        )
        select_plan.click()
    except WebDriverException as e:
        raise f'select_plan: {e}'

    try:
        email = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#email'))
        )
        email.click()
        email.send_keys(random.choice(email_list))
    except WebDriverException as e:
        raise f'enter_email: {e}'
    
    try:
        phone = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#phoneNumber'))
        )
        phone.click()
        phone.send_keys(mobile)
    except WebDriverException as e:
        raise f'enter_mobile: {e}'
    
    try:
        # Use keyboard keys to navigate to bin collection dropdown menu
        # random_weekday() function selects a random weekday
        ActionChains(driver)\
            .key_down(Keys.TAB)\
            .key_up(Keys.TAB)\
            .key_down(Keys.ARROW_DOWN)\
            .send_keys(random_weekday())\
            .key_down(Keys.ENTER)\
            .key_up(Keys.ENTER)\
            .perform()
    except WebDriverException as e:
        raise f'bin_collection_day: {e}'
    
    try:
        # Select bin(s)
        if plan == 'bronze' or plan == 'one-off':
            ActionChains(driver)\
                .key_down(Keys.TAB)\
                .key_up(Keys.TAB)\
                .key_down(Keys.ARROW_DOWN)\
                .send_keys(random_bin_selection())\
                .perform()
                #.key_down(Keys.ENTER)\
                #.key_up(Keys.ENTER)\
                
        else:
            pass
    except WebDriverException as e:
        raise f'select_bin: {e}'

    try:
        card = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#cardNumber'))
        )
        card.click()
        card.send_keys(success_card)
    except WebDriverException as e:
        raise f'enter_card_number: {e}'
    
    try:
        expiry_date = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#cardExpiry'))
        )
        expiry_date.click()
        expiry_date.send_keys(expiry)
    except WebDriverException as e:
        raise f'enter_expiry_date: {e}'

    try:
        cvc_number = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#cardCvc'))
        )
        cvc_number.click()
        cvc_number.send_keys(cvc)
    except WebDriverException as e:
        raise f'enter_cvc_number: {e}'
    
    try:
        card_name = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#billingName'))
        )
        card_name.click()
        card_name.send_keys(random.choice(name_list))
    except WebDriverException as e:
        raise f'enter_card_name: {e}'

    try:
        street_address = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#billingAddressLine1'))
        )
        street_address.click()
        street_address.send_keys(street)
    except WebDriverException as e:
        raise f'enter_street_address: {e}'

    try:
        # Use keyboard keys to navigate address details
        # The auto-complete feature gets in the way
        # This can be resolved by using the TAB key
        ActionChains(driver)\
            .key_down(Keys.ENTER)\
            .key_up(Keys.ENTER)\
            .perform()
            #.key_down(Keys.TAB)\
            #.key_up(Keys.TAB)\
    except WebDriverException as e:
        raise f'enter_suburb - Dropdown: {e}'

    try:    
        suburb_name = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#billingLocality'))
        )
        suburb_name.click()
        suburb_name.send_keys(suburb)
    except WebDriverException as e:
        raise Exception(f'enter_suburb: {e}')
    
    try:
        # Use keyboard keys to navigate to State dropdown menu
        # Selects w for WA
        ActionChains(driver)\
            .key_down(Keys.TAB)\
            .key_up(Keys.TAB)\
            .key_down(Keys.ARROW_DOWN)\
            .send_keys('w')\
            .key_down(Keys.ENTER)\
            .key_up(Keys.ENTER)\
            .perform()

        ActionChains(driver)\
            .key_down(Keys.ENTER)\
            .key_up(Keys.ENTER)\
            .perform()
    except WebDriverException as e:
        raise f'enter_state: {e}'
    
    try:
        post_code = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#billingPostalCode'))
        )
        post_code.click()
        post_code.send_keys(postcode)
    except WebDriverException as e:
        raise Exception(f'enter_postcode: {e}')

    try:
        ActionChains(driver)\
            .key_down(Keys.ENTER)\
            .key_up(Keys.ENTER)\
            .perform()
    except WebDriverException as e:
        raise Exception(f'enter_postcode - Pressing Enter: {e}')
    
    try:
        subscribe = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'SubmitButton SubmitButton--incomplete'))
        )
        subscribe.click()
        print(f'{plan} plan submitted')
        WebDriverWait(driver, 20).until(EC.url_contains("unitedpropertyservices.au/wheelie-wash-subscribed/?session_id"))
        driver.quit()
    except WebDriverException as e:
        print(f'subscribe: {e}')
        #raise Exception(f'subscribe: {e}')

    driver.quit()

    #if WebDriverException is True or Exception is True:
    #    driver.quit()




gold = 'gold'
silver = 'silver'
bronze = 'bronze'
one_off = 'one-off'

"""checkout_test(bronze)
sleep.sleep(20)
checkout_test(silver)
sleep.sleep(20)
checkout_test(gold)
sleep.sleep(20)
checkout_test(one_off)
"""


#for _ in range(4):
#    checkout_test(bronze, local)
#    sleep.sleep(5)
#    checkout_test(one_off, local)
#   sleep.sleep(5)
##    checkout_test(silver, local)
#    sleep.sleep(5)
#    checkout_test(gold, local)

#checkout_test(gold)
#driver = webdriver.Firefox(options=options) # Create a WebDriver instance with FirefoxDriver and the custom optio


"""gold_sub = ChoosePlan(driver, public, gold)
gold_sub.load_url()
gold_sub.select_plan()
gold_cus = CustomerDetails(driver, gold)
gold_cus.enter_email()
gold_cus.enter_mobile()
gold_cus.bin_collection_day()
gold_cus.select_bin()
gold_cus.enter_card_number()
gold_cus.enter_expiry_date()
gold_cus.enter_cvc_number()
gold_cus.enter_card_name()
gold_cus.enter_street_address()
gold_cus.enter_suburb()
gold_cus.enter_state()
gold_cus.enter_postcode()
gold_cus.subscribe()"""






if __name__ == '__main__':
    for _ in range(30):
        checkout_test(gold, local)
        sleep.sleep(2)
        checkout_test(silver, local)
        sleep.sleep(2)
        #checkout_test(bronze, local)


