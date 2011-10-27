.. _amazon:

.. _Boto: http://code.google.com/p/boto/

=========
Amazon
=========

Amazon is package of utilities to work with Amazon Web Services (AWS). It is
composed of serveral separate tools:

    * **AWS branded scripts** - bundled only for easier access as their documentation is somehow confusing
    * **SES SMTP relay** - implementation of SMTP server that forwards incoming mail messages to Amazon SES (simple e-mail service) via `Boto` library
    * **SMTP relay daemon** - Python executable which will daemonize when executed. Works as support for SMTP relay to use it as service on servers.
    
AWS branded scripts
===================
Scripts are written in Perl and require following .deb packages to be installed:

    * libxml-libxml-perl
    * libssl-dev

Most of the scripts also require you to have valid Amazon AWS credentials. It's
easier to put them in the file in your home directory. Example content of the
file goes like this::

    AWSAccessKeyId=YOUR_KEY_ID
    AWSSecretKey=YOUR_SECRET_KEY

These consist of following:

``ses-verify-email-address.pl``

    Use to verify e-mail addresses with Amazon SES. Example usage::
    
        ./ses-verify-email-address.pl -k ~/.amazon_aws.cred -v example@email.com
        

SES SMTP relay
================

.. py:class:: SESRelaySMTPServer(smtpd.SMTPServer)

    This is very simple Python implementation of SMTP server. The only thing
    it does is to forward the messages to `Boto` library, which is a Python interface
    for Amazon Web Services.

    .. py:method:: __init__(localaddr, remoteaddr, aws_key, aws_secret)
    
        :param localaddr: same as in ``smtp.SMTPServer``
        :param remoteaddr: same as in ``smtp.SMTPServer``
        :param aws_key: ID key to your AWS account
        :param aws_secret: Secret key to your AWS account
    

SMTP relay daemon
=================

Daemon can be used to run SMTP relay server as a service in unix-like environments.
It expects Debian distribution though.

Steps to run the service are following:

    #. Install fragapy library from sources repository. Install boto library.
    #. Make symlink of smtpreldaemon.py to /usr/sbin/smtpreldaemon
    #. Copy smtp_relay.sh to /etc/init.d
    #. Create user amazon.
    #. Create /home/amazon/.smtpreldaemon.cfg and edit configuration. You can take smtpreldaemon.cfg as template.
    #. Set permissions to chosen config files to amazon user.
    #. Install daemon: update-rc.d smtp_relay.sh defaults
    
Last step ensures that the ``smtp_relay.sh`` will be run on startup of the 
server automatically so you don't need to care about it.
