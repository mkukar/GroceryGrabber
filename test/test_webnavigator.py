
# tests for webnavigator class
# NOTE - Integration tests require valid credentials, internet connection, etc.
# Copyright Michael Kukar 2020

import json, sys
import unittest

sys.path.append("..")
from webnavigator import WebNavigator

class IntegrationTestCases(unittest.TestCase):

    CONFIG_FILE = "../config.json"

    def setUp(self):
        # reads config file for valid credentials
        data = None
        with open(self.CONFIG_FILE) as f:
            data = json.load(f)
        try:
            self.PRIMENOW_USER = data['carts'][0]['user']
            self.PRIMENOW_PASS = data['carts'][0]['pass']
        except Exception as e:
            print(e)
        
        self.wn = WebNavigator()
        self.browser = self.wn.getBrowser()

    def tearDown(self):
        self.browser.close()

    def test_loginsucceedswithvalidcredentialsForPrimeNow(self):
        # all amazon accounts are the same, so only check one
        self.assertTrue(self.wn.login("PRIMENOW_AMAZON", self.browser, self.PRIMENOW_USER, self.PRIMENOW_PASS))

    def test_checkIfDeliveryTimeAvailable(self):
        # all amazon use same acct, only need one login
        self.wn.login("PRIMENOW_AMAZON", self.browser, self.PRIMENOW_USER, self.PRIMENOW_PASS)
        # since we dont know if there is a slot or not, just makes sure there was no error reported
        result = self.wn.checkIfDeliveryTimeAvailable("PRIMENOW_AMAZON", self.browser)
        print(result[1])
        self.assertFalse("ERROR" in result[1])
        result = self.wn.checkIfDeliveryTimeAvailable("PRIMENOW_WHOLE_FOODS", self.browser)
        print(result[1])
        self.assertFalse("ERROR" in result[1])

if __name__ == "__main__":
    unittest.main()