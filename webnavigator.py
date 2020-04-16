# navigates web pages for the grocerygrabber
# Copyright Michael Kukar 2020. 

import sys, os, time
import subprocess
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options

class WebNavigator:

    SITE_INFO_DICT = {
        'PRIMENOW_AMAZON' : {
            'login_link' : 'https://primenow.amazon.com/signin?returnUrl=https://primenow.amazon.com/home',
            'user_id' : 'ap_email',
            'pass_id' : 'ap_password',
            'submit_id' : 'signInSubmit',
            'cart_link' : 'https://primenow.amazon.com/checkout/enter-checkout?merchantId=AQCUSYIS91P2B',
            'delivery_options_id' : 'delivery-slot-form',
            'no_delivery_text' : 'No delivery windows available.'
        },
        'PRIMENOW_WHOLE_FOODS' : {
            'login_link' : 'https://primenow.amazon.com/signin?returnUrl=https://primenow.amazon.com/home',
            'user_id' : 'ap_email',
            'pass_id' : 'ap_password',
            'submit_id' : 'signInSubmit',
            'cart_link' : 'https://primenow.amazon.com/checkout/enter-checkout?merchantId=A292AGRFD023A8',
            'delivery_options_id' : 'delivery-slot-form',
            'no_delivery_text' : 'No delivery windows available.'
        },
        'PRIMENOW_KEG_N_BOTTLE' : {
            'login_link' : 'https://primenow.amazon.com/signin?returnUrl=https://primenow.amazon.com/home',
            'user_id' : 'ap_email',
            'pass_id' : 'ap_password',
            'submit_id' : 'signInSubmit',
            'cart_link' : 'https://primenow.amazon.com/checkout/enter-checkout?merchantId=A2LMB8A37PW4SX',
            'delivery_options_id' : 'delivery-slot-form',
            'no_delivery_text' : 'No delivery windows available.'
        },
        'PRIMENOW_BRISTOL_FARMS' : {
            'login_link' : 'https://primenow.amazon.com/signin?returnUrl=https://primenow.amazon.com/home',
            'user_id' : 'ap_email',
            'pass_id' : 'ap_password',
            'submit_id' : 'signInSubmit',
            'cart_link' : 'https://primenow.amazon.com/checkout/enter-checkout?merchantId=A2V56U6DPP6YTA',
            'delivery_options_id' : 'delivery-slot-form',
            'no_delivery_text' : 'No delivery windows available.'
        }
    }

    # creates a website browser object based on firefox
    # geckodriver_exe : name of geckodriver executable that must be in path
    # return          : firefox website browser object
    def getBrowser(self, geckodriver_exe=r"geckodriver_0_26_0_win64.exe"):
        opts = Options()
        #opts.headless = True # removed so we can do manual login and modifications
        return Firefox(executable_path=geckodriver_exe, options=opts)

    # allows the user to manually log in within a certain timeout
    # site_id  : name of site in SITE_INFO_DICT
    # browser  : browser object
    # timeout  : (optional) time to wait for user to log in
    # return   : true on success, false on failure
    def manualLogin(self, site_id, browser, timeout=60):
        if site_id not in self.SITE_INFO_DICT.keys():
            return False
        loginTitle = browser.title

        browser.get(self.SITE_INFO_DICT[site_id]['login_link'])
        time.sleep(timeout)

        if browser.title == loginTitle: # did not change pages
            return False
        else:
            return True

    # automatically logs into a given site
    # site_id                : name of site in SITE_INFO_DICT
    # browser                : browser object
    # username               : account username
    # password               : account password
    # time_to_manually_retry : (optional) if given, lets the user retry for X amount of seconds
    # return                 : true on success, false on failure
    def login(self, site_id, browser, username, password, time_to_manually_retry=30):
        if site_id not in self.SITE_INFO_DICT.keys():
            return False
        # loads the login website
        browser.get(self.SITE_INFO_DICT[site_id]['login_link'])
        loginTitle = browser.title
        try:
            # enters credentials into the login fields
            time.sleep(3) # these delays are to make amazon think we are human
            browser.find_element_by_id(self.SITE_INFO_DICT[site_id]['user_id']).send_keys(username)
            time.sleep(3)
            browser.find_element_by_id(self.SITE_INFO_DICT[site_id]['pass_id']).send_keys(password)
            time.sleep(3)
            # clicks the enter button
            browser.find_element_by_id(self.SITE_INFO_DICT[site_id]['submit_id']).click()
        except:
            if "sign-in" in loginTitle.lower():
                return False
            else:
                # already logged in, just redirected to home page
                return True

        # if title stays the same as sign-in, then error occured (didn't redirect to main page)
        if browser.title == loginTitle and "sign-in" in loginTitle.lower():
            if time_to_manually_retry != 0:
                # gives you a chance to type in the password yourself
                time.sleep(time_to_manually_retry)
                if browser.title != loginTitle:
                    return True
            print(browser.title)
            print(loginTitle)
            return False
        else:
            return True

    # determines if delivery time is available
    # site_id           : name of site
    # browser           : web browser object
    # tryLoginOnFailure : (optional) if true will try auto-login if an error occurs (logged out of cart)
    # return            : tuple of (True/False if deliver time found, string of time(s)/error message)
    def checkIfDeliveryTimeAvailable(self, site_id, browser, tryLoginOnFailure=False, username=None, password=None):
        if site_id not in self.SITE_INFO_DICT.keys():
            return (False, "ERROR - unsupported site")
        
        # assumes you are already logged in
        browser.get(self.SITE_INFO_DICT[site_id]['cart_link'])
        delivery_slots = None
        try:
            delivery_slots = browser.find_element_by_id(
                self.SITE_INFO_DICT[site_id]['delivery_options_id']
            )
        except Exception as e:
            if tryLoginOnFailure:
                # tries loging in max of two times
                if not self.login(site_id, browser, username, password):
                    self.login(site_id, browser, username, password)
                # note - only will try auto-login once, then will just fail second time
                return self.checkIfDeliveryTimeAvailable(site_id, browser, tryLoginOnFailure=False, username=username, password=password)
            return (False, "ERROR - Could not find delivery option")

        if self.SITE_INFO_DICT[site_id]['no_delivery_text'] in delivery_slots.text:
            return (False, "No slots")
        else:
            return (True, delivery_slots.text)
        
