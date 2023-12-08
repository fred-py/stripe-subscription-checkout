"""Selenium Indexed Documentation""" 
# https://selenium-python.readthedocs.io/

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options  # Set up the drive to handle downloads.
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException

options = Options()  # Create a new options folder
#options.add_argument("--headless")  # Run headless

email = 'marketing@unitedpropertyservices.au'
key = '9028'
mobile = '+61404221122'

name = 'Samuel Jackson'


def add_customer():
    """Add customer to ServiceM8 job.
    Selenium is as this operation is not supported by the API."""
    driver = webdriver.Firefox(options=options) # Create a WebDriver instance with FirefoxDriver and the custom options
    try:
        driver.get("https://www.servicem8.com/au/login-page")
    except WebDriverException as e:
        print(f"Error Accessing the URL {e} , the script will run again in 4 minutes")
        #time.sleep(4)
        #retry_login(driver, max_retries=5, delay_seconds=60)
    
    e = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#user_email'))
    )
    e.send_keys(email)

    p = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#user_password'))
    )
    p.send_keys(key)

    login = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'login-button'))
    )
    login.click()

    search_job(driver, mobile)

    driver.quit()


def search_job(driver, mobile):
    try:
        # Dispatch Board Button
        d = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (
                    By.ID, 'PluginGraphicMenuSystem_MenuItem_DispatchBoard'
                )
            )
        )
        d.click()

        search = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR, '#PluginGlobalSearch_Icon'
                )
            )
        )
        search.click()

        # Wait until the obscuring element disappears
        WebDriverWait(driver, 20).until(EC.invisibility_of_element((By.ID, 'PluginJobDispatch_LoadingMask')))

        search_field = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#PluginGlobalSearch_SearchPage_SearchInput'))
        )
        search_field.click()
        search_field.send_keys(mobile)

        results = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'PluginGlobalSearch_SearchResult'))
        )
        results.click()

        # Wait until the obscuring element disappears
        #========
        customer = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#PluginJobDispatchManageJobForm_CustomerName'))
        )
        customer.click()
        customer.send_keys(name)

        save = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#PluginJobDispatchManageJobForm_SaveButton'))
        )
        save.click()

    except Exception as e:
        print(f"FFS: {e}")


if __name__ == "__main__":
    add_customer()