#!/usr/bin/env python
'''
Created on 20.10.2011

@author: xaralis
'''
import asyncore, sys, os, ConfigParser

from fragapy.unix.deamonize import Daemon
from fragapy.amazon.smtp_relay import SESRelaySMTPServer

class SESRelaySMTPDaemon(Daemon):
    def __init__(self, pidfile):
        config = ConfigParser.SafeConfigParser()
        cfg_path = os.path.expanduser('~/.smtpreldaemon.cfg')
        
        if not os.path.exists(cfg_path):
            sys.stderr.write(u"Missing configuration file, %s does not exist." % cfg_path)
            sys.stderr.flush()
            sys.exit(2)
            
        config.readfp(open(cfg_path))
        self.ip_addr = config.get('remote', 'ip_addr')
        self.port = config.getint('remote', 'port')
        self.key = config.get('credentials', 'key')
        self.secret = config.get('credentials', 'secret')
        
        stderr_log = None
        stdout_log = None
        
        if config.has_section('log'):
            if config.has_option('log', 'errors'):
                stderr_log = config.get('log', 'errors')
            if config.has_option('log', 'stdout'):
                stdout_log = config.get('log', 'stdout')
        
        if stderr_log is None:
            stderr_log = '/var/log/amazon/error.log'
        if stdout_log is None:
            stdout_log = '/dev/null'

        super(SESRelaySMTPDaemon, self).__init__(pidfile, stdout=stdout_log, stderr=stderr_log)
        
        if not self.key and not self.secret:
            sys.stderr.write("Missing credentials to use for AWS")
            sys.stderr.flush()
            sys.exit(2)
    
    def run(self):
        sys.stdout.write(u"Running SMTP relay service on %s:%s ..." % (self.ip_addr, self.port))
        sys.stdout.flush()
        SESRelaySMTPServer((self.ip_addr, self.port), None, self.key, self.secret)
        asyncore.loop()
        
        
if __name__ == '__main__':
    d = SESRelaySMTPDaemon('/tmp/smtpreldaemon.pid')
    d.start()
    