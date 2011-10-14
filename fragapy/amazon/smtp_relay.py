#!/usr/bin/env python
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

import smtpd, sys, asyncore, optparse
from email.parser import Parser

try:
    from boto.ses.connection import SESConnection
except ImportError:
    print "This script needs boto library. Use pip install boto to get it."
    sys.exit(2)

class SESRelaySMTPServer(smtpd.SMTPServer):
    def __init__(self, localaddr, remoteaddr, aws_key, aws_secret):
        smtpd.SMTPServer.__init__(self, localaddr, remoteaddr)
        self.aws_key = aws_key
        self.aws_secret = aws_secret

    def process_message(self, peer, mailfrom, rcpttos, data):
        #Print the request information
        print 'Receiving message from:', peer
        print 'Message addressed from:', mailfrom
        print 'Message addressed to :', rcpttos
        print 'Message length :', len(data)
        
        # Parse the message and remove headers that are offensive to SES
        msg = Parser().parsestr(data)
        if 'Errors-To' in msg:
            del msg['Errors-To']
        
        # Send out via SES
        connection = SESConnection(aws_access_key_id=self.aws_key,
            aws_secret_access_key=self.aws_secret)
        connection.send_raw_email(mailfrom, msg.as_string())


def main():
    usage = "usage: %prog [options]"
    parser = optparse.OptionParser(usage)
    parser.add_option("-p", "--port", dest="port",
                    action="store",
                    type="int",
                    default=1025,
                    help="port to run on")
    parser.add_option("-a", "--addr", dest="ip_addr",
                    action="store",
                    type="string",
                    default='',
                    help="IP address to run on")
    parser.add_option("-k", "--aws-key", dest="key",
                    action="store",
                    default='',
                    help="AWS key")
    parser.add_option("-s", "--aws-secret", dest="secret",
                    action="store",
                    default='',
                    help="AWS secret key")
    options, args = parser.parse_args()
    
    port, ip_addr, key, secret = options.port, options.ip_addr, options.key, options.secret
    
    if not key and not secret:
        print "Missing credentials to use for AWS"
        sys.exit(2)
        
    try:
        server = SESRelaySMTPServer((ip_addr, port), None, key, secret)
        asyncore.loop()
    except KeyboardInterrupt:
        sys.exit(1)
    
if __name__ == '__main__':
    main()
    