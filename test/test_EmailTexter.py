# unit tests for emailtexter
# CB: Michael Kukar 2020
# Copyright Michael Kukar 2020. All Rights Reserved.

import json, sys
import unittest

sys.path.append("..")
from emailtexter import EmailTexter

class IntegrationTestCases(unittest.TestCase):

    CONFIG_FILE = "../config.json"

    VALID_EMAIL = ""
    INVALID_EMAIL = "notarealemail"

    VALID_MESSAGE = "this is not a drill"
    EMPTY_MESSAGE = ""

    VALID_SUBJECT = "hello there"
    VALID_FROM = "donotreply@me.com"

    VALID_EMAIL_USERNAME = ""
    VALID_EMAIL_PASSWORD = ""
    VALID_EMAIL_URL = ""

    INVALID_EMAIL_USERNAME = "notarealemail"
    INVALID_EMAIL_PASSWORD = "changeme1"
    INVALID_EMAIL_URL = "not.a.real.url"
    INVALID_EMAIL_PORT = 9999

    def setUp(self):
        self.et = EmailTexter()

        # reads config file for valid credentials
        data = None
        with open(self.CONFIG_FILE) as f:
            data = json.load(f)
        try:
            self.VALID_EMAIL = self.et.getPhoneNumberEmailAddress(
                data['phone_credentials']['number'],
                data['phone_credentials']['carrier']
            )
            self.VALID_EMAIL_USERNAME = data['email_credentials']['user']
            self.VALID_EMAIL_PASSWORD = data['email_credentials']['pass']
            self.VALID_EMAIL_URL = data['email_credentials']['url']
        except Exception as e:
            print(e)

        # creates necessary objects
        self.server = self.et.initializeEmailServer(
            self.VALID_EMAIL_USERNAME,
            self.VALID_EMAIL_PASSWORD,
            self.VALID_EMAIL_URL
        )
    
    def tearDown(self):
        self.server.close()
    
    def test_initializeEmailServerSucceedsWithValidParams(self):
        self.server.close()
        server = self.et.initializeEmailServer(
            self.VALID_EMAIL_USERNAME,
            self.VALID_EMAIL_PASSWORD,
            self.VALID_EMAIL_URL
            )
        self.assertIsNotNone(server)
        server.close()
    
    def test_initializeEmailServerReturnsNoneOnInvalidUsername(self):
        self.assertIsNone(self.et.initializeEmailServer(
            self.INVALID_EMAIL_USERNAME,
            self.VALID_EMAIL_PASSWORD,
            self.VALID_EMAIL_URL
        ))
    
    def test_initializeEmailServerReturnsNoneOnInvalidPassword(self):
        self.assertIsNone(self.et.initializeEmailServer(
            self.VALID_EMAIL_USERNAME,
            self.INVALID_EMAIL_PASSWORD,
            self.VALID_EMAIL_URL
        ))
    
    def test_initializeEmailServerReturnsNoneOnInvalidUrl(self):
        self.assertIsNone(self.et.initializeEmailServer(
            self.VALID_EMAIL_USERNAME,
            self.VALID_EMAIL_PASSWORD,
            self.INVALID_EMAIL_URL
        ))
    
    def test_initializeEmailServerReturnsNoneOnInvalidPort(self):
        self.assertIsNone(self.et.initializeEmailServer(
            self.VALID_EMAIL_USERNAME,
            self.VALID_EMAIL_PASSWORD,
            self.VALID_EMAIL_URL,
            port=self.INVALID_EMAIL_PORT
        ))
    
    def test_sendMessageSucceedsWithValidEntries(self):
        self.assertTrue(self.et.sendMessage(
            self.VALID_EMAIL,
            self.VALID_MESSAGE, 
            self.server)
        )

    def test_sendMessageFailsWithInvalidEmailAddress(self):
        self.assertFalse(self.et.sendMessage(
            self.INVALID_EMAIL, 
            self.VALID_MESSAGE, 
            self.server)
        )
    
    def test_sendMessageFailsWithEmptyMessage(self):
        self.assertFalse(self.et.sendMessage(
            self.VALID_EMAIL, 
            self.EMPTY_MESSAGE, 
            self.server)
        )
    
    def test_sendMessageSucceedsWithValidSubject(self):
        self.assertTrue(self.et.sendMessage(
            self.VALID_EMAIL, 
            self.VALID_MESSAGE, 
            self.server, 
            subject=self.VALID_SUBJECT)
        )
    
    def test_sendMessageSucceedsWithValidFromEmail(self):
        self.assertTrue(self.et.sendMessage(
            self.VALID_EMAIL, 
            self.VALID_MESSAGE, 
            self.server, 
            fromEmail=self.VALID_FROM)
        )

    def test_sendMessageSucceedsWithAllOptionalParametersSet(self):
        self.assertTrue(self.et.sendMessage(
            self.VALID_EMAIL, 
            self.VALID_MESSAGE, 
            self.server, 
            subject=self.VALID_SUBJECT, 
            fromEmail=self.VALID_FROM)
        )


class UnitTestCases(unittest.TestCase):

    CONFIG_FILE = '../config.json'

    VALID_PHONE_NUMBER = ''
    VALID_PHONE_CARRIERS = list(EmailTexter.SUPPORTED_CARRIERS.keys())

    INVALID_PHONE_NUMBER = '000'
    INVALID_PHONE_CARRIER = 'verizonmobile&t'

    def setUp(self):
        self.et = EmailTexter()

        # reads config file for valid credentials
        data = None
        with open(self.CONFIG_FILE) as f:
            data = json.load(f)
        try:
            self.VALID_PHONE_NUMBER = data['phone_credentials']['number']
        except Exception as e:
            print(e)
        

    def test_getPhoneNumberEmailAddressReturnsValidEmailWithValidData(self):
        # only check no errors for all carriers, we compare string for just one default case
        for carrier in self.VALID_PHONE_CARRIERS:
            self.assertIsNotNone(self.et.getPhoneNumberEmailAddress(self.VALID_PHONE_NUMBER, carrier))
        self.assertEqual(
            self.VALID_PHONE_NUMBER + "@vtext.com", 
            self.et.getPhoneNumberEmailAddress(self.VALID_PHONE_NUMBER, "VERIZON")
        )
    
    def test_getPhoneNumberEmailAddressReturnsNoneWithInvalidPhoneNumber(self):
        self.assertIsNone(
            self.et.getPhoneNumberEmailAddress(
                self.INVALID_PHONE_NUMBER, 
                self.VALID_PHONE_CARRIERS[0]
            )
        )

    def test_getPhoneNumberEmailAddressReturnsNoneWithInvalidCarrier(self):
        self.assertIsNone(
            self.et.getPhoneNumberEmailAddress(
                self.VALID_PHONE_NUMBER, 
                self.INVALID_PHONE_CARRIER
            )
        )


if __name__ == "__main__":
    unittest.main()