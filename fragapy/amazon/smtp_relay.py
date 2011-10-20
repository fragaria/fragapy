'''
Created on 14.10.2011

@author: xaralis

SMTP->SES Relay Server w/ Header Filter

A Lightweight SMTP server that accepts all messages, removes the Error-To header
which offends SES, then relays them to SES

Credit to:
 - http://www.doughellmann.com/PyMOTW/smtpd/ for a tutorial on smtpd with asyncore
 - http://tech.loku.com/2011/08/17/smtp-relay-to-amazon-ses/ ses idea
'''

import smtpd, sys
from email.parser import Parser

try:
    from boto.exception import BotoServerError
    from boto.ses.connection import SESConnection
except ImportError:
    sys.stderr.write("This script needs boto library. Use pip install boto to get it.")
    sys.stderr.flush()
    sys.exit(2)

class SESRelaySMTPServer(smtpd.SMTPServer):
    def __init__(self, localaddr, remoteaddr, aws_key, aws_secret):
        smtpd.SMTPServer.__init__(self, localaddr, remoteaddr)
        self.aws_key = aws_key
        self.aws_secret = aws_secret

    def process_message(self, peer, mailfrom, rcpttos, data):
        # Print the request information
        sys.stdout.write(u"Receiving message from: %s\n" % str(peer))
        sys.stdout.write(u"Message addressed from: %s\n" % str(mailfrom))
        sys.stdout.write(u"Message addressed to: %s\n" % str(rcpttos))
        sys.stdout.write(u"Message length: %s\n" % str(len(data)))
        sys.stdout.flush()
        
        # Parse the message and remove headers that are offensive to SES
        msg = Parser().parsestr(data)
        if 'Errors-To' in msg:
            del msg['Errors-To']
        
        # Send out via SES
        try:
            connection = SESConnection(aws_access_key_id=self.aws_key,
                aws_secret_access_key=self.aws_secret)
            connection.send_raw_email(msg.as_string(), source=mailfrom)
        except BotoServerError, err:
            sys.stderr.write(str(err))
            sys.stdout.flush()
    
    