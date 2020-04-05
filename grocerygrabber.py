# Notifies when there is an available grocery delivery slot
# in popular delivery apps (amazon prime now, etc.)
# Copyright Michael Kukar 2020

VERSION = 1.0

import datetime, argparse, threading
import os, sys, json

from emailtexter import EmailTexter
from webnavigator import WebNavigator

class GroceryGrabber:

    #
    # VARIABLES
    #
    configFile = None
    verbose = False

    webBrowser = None
    emailTexter = None
    webNavigator = None
    emailServer = None
    emailAddr = None

    configData = None
    tickSeconds = None
    readConfigTickInterval = None
    currentReadConfigTick = None
    manualLogin = True
    enabledCarts = []
    credentials = {}

    #
    # CONSTRUCTOR/DESTRUCTOR
    #
    def __init__(self, configFile, verbose=False):
        self.configFile = configFile
        self.verbose=verbose
        self.emailTexter = EmailTexter()
        self.webNavigator = WebNavigator()

    def __del__(self):
        if self.webBrowser is not None:
            self.webBrowser.close()

    #
    # FUNCTIONS
    #

    # sets up all the objects
    def setup(self):
        if self.verbose: print("Setting up...")
        if not self.readConfig(self.configFile):
            return False
        self.webBrowser = self.webNavigator.getBrowser()
        if not self.authenticateAccounts(self.enabledCarts, self.webBrowser, manual=self.manualLogin):
            return False
        self.emailServer = self.emailTexter.initializeEmailServer(
            self.credentials['email']['user'],
            self.credentials['email']['pass'], 
            self.credentials['email']['url']
            )
        self.emailAddr = self.emailTexter.getPhoneNumberEmailAddress(
            self.credentials['phone']['number'], 
            self.credentials['phone']['carrier']
            )
        if self.verbose: print("Setup complete.")
        return True

    # reads in the config file and saves the data into memory
    def readConfig(self, configFile):
        if self.verbose: print("Reading configuration file...")
        # checks if file exists and is a json file
        if configFile is None or ".json" not in configFile:
            if self.verbose: print("ERROR: Config file invalid.")
            return False
        if not os.path.exists(configFile):
            if self.verbose: print("ERROR: Config file not found.")
            return False
        
        with open(configFile) as f:
            self.configData = json.load(f)

        try:
            self.tickSeconds = int(self.configData['check_cart_interval_secs'])
            self.readConfigTickInterval = int(self.configData['check_config_interval_mins']) * 60
            self.currentReadConfigTick = self.readConfigTickInterval

            self.enabledCarts = []
            for cart in self.configData['carts']:
                if cart['enabled']:
                    self.enabledCarts.append(dict(cart))

            self.credentials = {
                'email' : self.configData['email_credentials'],
                'phone' : self.configData['phone_credentials']
            }

            self.manualLogin = not self.configData['use_automatic_login']
        except Exception as e:
            if self.verbose: 
                print("ERROR: Could not read config file.")
                print(str(e))
            return False

        if self.verbose: print("Success.")
        return True

    # logs into each account in the account list, or gives the manual option (set period of time)
    def authenticateAccounts(self, accountList, browser, manual=True):
        result = True            
        if self.verbose: print("Authenticating accounts. Please be patient...")
        for account in accountList:
            if manual:
                result = result and self.webNavigator.manualLogin(account['website'], browser)
            else:
                result = result and self.webNavigator.login(account['website'], browser, account['user'], account['pass'])
        if result is False and self.verbose:
            print("Failed to authenticate.")
        elif self.verbose:
            print("Done.")
        return result

    # checks if delivery is available, periodically reloads the config, and automatically re-launches itself
    # NOTE - This function will run forever until interrupted
    def run(self):
        # first reads config if tick count reached
        if self.currentReadConfigTick <= 0:
            if self.verbose: print("Reloading config file...")
            self.readConfig(self.configFile)
            self.currentReadConfigTick = self.readConfigTickInterval
            if self.verbose: print("Done.")

        else:
            self.currentReadConfigTick -= 1

        # now checks each cart that is enabled
        if self.verbose: print("Checking availability " + str(datetime.datetime.now()))
        for cart in self.enabledCarts:
            availabilityResult = self.webNavigator.checkIfDeliveryTimeAvailable(cart['website'], self.webBrowser)
            # if found availability, sends a text
            if availabilityResult[0] == True:
                if self.verbose: print("Found availability for " + cart['website'] + "! Sending message...")
                self.emailTexter.sendMessage(self.emailAddr, "Availibility for " + cart['website'] + '!\n' + availabilityResult[1], self.emailServer)
                # now disable send availability for this one until config is read again
                self.enabledCarts.remove(cart)
            else:
                if self.verbose: print(str(availabilityResult[1]))

        if self.verbose: print("Done.")
        # repeats itself forever
        # NOTE - This causes difficulty in interrupting the process since it will only die once the timer has run out (e.g. if 60 seconds, would have to wait 60 seconds to die)
        threading.Timer(self.tickSeconds, self.run).start()
        

if __name__ == "__main__":
    # read command line input
    parser = argparse.ArgumentParser(
        description='Notifies when delivery windows are available for grocery delivery services',
        epilog='Copyright Michael Kukar 2020.'
        )

    parser.add_argument("-c", "--config", dest="config", default="config.json", help="json configuration file")
    parser.add_argument("-v", "--verbose", dest="verbose", action='store_true', help="prints detailed runtime info to console")

    args = parser.parse_args()

    verbose = args.verbose
    gb = GroceryGrabber(args.config, verbose=verbose)

    if verbose:
        print("Grocery Grabber v" + str(VERSION))
        print("\tConfig File : " + str(args.config))
        print("\tVerbose     : " + str(verbose))


    # sets up everything (logging into accounts, etc.)
    if not gb.setup():
        if not verbose:
            print("Error setting up. Run with --verbose to see details.")
        else:
            print("Error setting up.")
        sys.exit(1)

    # runs until cancelled. Config can be updated in meantime
    gb.run()
