# sends "texts" through an email
# CB: Michael Kukar 2020

import smtplib
from email.message import EmailMessage

class EmailTexter:

    SUPPORTED_CARRIERS = {
        'VERIZON' : 'vtext.com',
        'TMOBILE' : 'tmomail.net'
    }

    # gets the smtp server object to send emails
    # NOTE - uses SSL
    # username : email username
    # password : email password
    # smtpUrl  : url of smtp server
    # port     : (optional) port of smtp server
    # return   : smtplib server object, or None on error
    def initializeEmailServer(self, username, password, smtpUrl, port=465):
        try:
            server = smtplib.SMTP_SSL(smtpUrl, port)
            server.ehlo()
            server.login(username, password)
        except Exception as e:
            # TODO - ADD ERROR HANDLING/PRINTING
            return None
        return server
 
    # creates email address from phone number
    # phoneNumber : 10 digit string phone number e.g. 5551234567
    # carrier     : carrier name from SUPPORTED_CARRIERS keys
    # return      : email address string or None on error
    def getPhoneNumberEmailAddress(self, phoneNumber, carrier):
        if carrier not in self.SUPPORTED_CARRIERS.keys():
            return None
        elif len(phoneNumber) != 10:
            return None
        return str(phoneNumber) + '@' + self.SUPPORTED_CARRIERS[carrier]
    
    # sends email from phone number
    # emailAddr : email to send to
    # message   : message to send
    # server    : smtp server object
    # fromEmail : (optional) email to put as "from"
    # subject   : (optional) email subject to add
    # return    : true on success, false on fail
    def sendMessage(self, emailAddr, message, server, fromEmail='donotreply@GroceryGrabber.py', subject=None):
        msg = EmailMessage()
        # requires message and server
        if message is None or len(message) == 0:
            return False
        if server is None:
            return False
        # makes sure email is valid-ish (contains @ and the right side as a '.' as in .com)
        if '@' not in emailAddr or '.' not in emailAddr.split('@')[1]:
            return False
        if subject is not None:
            msg['Subject'] = subject
        msg['From'] = fromEmail
        msg['To'] = emailAddr
        msg.set_content(message)
        server.send_message(msg)
        return True

