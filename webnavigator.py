# navigates web pages for the grocerygrabber
# CB: Michael Kukar 2020
# Copyright Michael Kukar 2020. All Rights Reserved.

import sys, os, time
import subprocess
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options

class WebNavigator:

    SUPPORTED_SITES = ['PRIMENOW_AMAZON', 'PRIMENOW_WHOLE_FOODS']

    LOGIN_URL_DICT = {
        'PRIMENOW_AMAZON' : "https://primenow.amazon.com/signin?returnUrl=https://primenow.amazon.com/home",
        'PRIMENOW_WHOLE_FOODS' : "https://primenow.amazon.com/signin?returnUrl=https://primenow.amazon.com/home"

    }

    LOGIN_FIELD_DICT = {
        'PRIMENOW_AMAZON' : {
            'user' : 'ap_email',
            'pass' : 'ap_password',
            'submit' : 'signInSubmit'
        },
        'PRIMENOW_WHOLE_FOODS' : {
            'user' : 'ap_email',
            'pass' : 'ap_password',
            'submit' : 'signInSubmit'
        }
    }

    CART_DICT = {
        'PRIMENOW_AMAZON' : {
            'cart_link' : 'https://primenow.amazon.com/checkout/enter-checkout?merchantId=AQCUSYIS91P2B',
            'delivery_options_id' : 'delivery-slot-form',
            'no_delivery_text' : 'No delivery windows available.'
        },
        'PRIMENOW_WHOLE_FOODS' : {
            'cart_link' : 'https://primenow.amazon.com/checkout/enter-checkout?merchantId=A292AGRFD023A8',
            'delivery_options_id' : 'delivery-slot-form',
            'no_delivery_text' : 'No delivery windows available.'
        }
    }

    # creates a website driver to use to load websites
    def getBrowser(self, geckodriver_exe=r"geckodriver_0_26_0_win64.exe"):
        opts = Options()
        #opts.headless = True
        return Firefox(executable_path=geckodriver_exe, options=opts)


    def login(self, site_id, browser, username, password, time_to_manually_retry=0):
        if site_id not in self.SUPPORTED_SITES:
            return False
        # loads the login website
        browser.get(self.LOGIN_URL_DICT[site_id])
        loginTitle = browser.title

        # enters credentials into the login fields
        time.sleep(3) # these delays are to make amazon think we are human
        browser.find_element_by_id(self.LOGIN_FIELD_DICT[site_id]['user']).send_keys(username)
        time.sleep(3)
        browser.find_element_by_id (self.LOGIN_FIELD_DICT[site_id]['pass']).send_keys(password)
        time.sleep(3)
        # clicks the enter button
        browser.find_element_by_id(self.LOGIN_FIELD_DICT[site_id]['submit']).click()

        # if title stays the same as sign-in, then error occured (didn't redirect to main page)
        if browser.title == loginTitle:
            if time_to_manually_retry != 0:
                # gives you a chance to type in the password yourself
                time.sleep(time_to_manually_retry)
                if browser.title != loginTitle:
                    return True
            return False
        else:
            return True


    # return tuple of True/False if delivery time found, and then the string of the time(s)
    def checkIfDeliveryTimeAvailable(self, site_id, browser):
        if site_id not in self.SUPPORTED_SITES:
            return (False, "ERROR - unsupported site")
        
        # assumes you are already logged in
        browser.get(self.CART_DICT[site_id]['cart_link'])
        delivery_slots = None
        try:
            delivery_slots = browser.find_element_by_id(
                self.CART_DICT[site_id]['delivery_options_id']
            )
        except Exception as e:
            return (False, "ERROR - Could not find delivery option")

        if self.CART_DICT[site_id]['no_delivery_text'] in delivery_slots.text:
            return (False, "No slots")
        else:
            return (True, delivery_slots.text)
        
