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

import smtpd, sys, asyncore, ConfigParser, os
from email.parser import Parser
from fragapy.unix.deamonize import Daemon

try:
    from boto.exception import BotoServerError
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


class SESRelaySMTPDaemon(Daemon):
    def __init__(self, pidfile, ip_addr, port, key, secret, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
        super(SESRelaySMTPDaemon, self).__init__(pidfile, stdin, stdout, stderr)
        self.ip_addr = ip_addr
        self.port = port
        self.key = key
        self.secret = secret
    
    def run(self):
        print u"Running SMTP relay service on %s:%s ..." % (self.ip_addr, self.port)
        SESRelaySMTPServer((self.ip_addr, self.port), None, self.key, self.secret)
        asyncore.loop()


def main():
    config = ConfigParser.SafeConfigParser()
    cfg_path = os.path.expanduser('~/.ses_smtp_relay.cfg')
    
    if not os.path.exists(cfg_path):
        print u"Missing configuration file, %s does not exist." % cfg_path
        sys.exit(2)
        
    config.readfp(open(cfg_path))
    ip_addr = config.get('remote', 'ip_addr')
    port = config.getint('remote', 'port')
    key = config.get('credentials', 'key')
    secret = config.get('credentials', 'secret')
    
    error_log = None
    stdout_log = None
    
    if config.has_section('log'):
        if config.has_option('log', 'errors'):
            error_log = config.get('log', 'errors')
        if config.has_option('log', 'stdout'):
            stdout_log = config.get('log', 'stdout')
    
    if error_log is None:
        error_log = '/tmp/ses_smtp_relay.error.log'
    if stdout_log is None:
        stdout_log = '/dev/null'
    
    if not key and not secret:
        print "Missing credentials to use for AWS"
        sys.exit(2)
        
    daemon = SESRelaySMTPDaemon('/tmp/ses_smtp_relay.pid', ip_addr, port, key, secret, stdout=stdout_log, stderr=error_log)
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)
    
    
if __name__ == "__main__":
    main()
    
    