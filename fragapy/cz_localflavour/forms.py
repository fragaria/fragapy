'''
Created on 17.9.2010

@author: xaralis
'''
from django.forms.fields import CharField
from django.utils.translation import ugettext_lazy as _

import validators

class CzICField(CharField):
    default_error_messages = {
        'invalid': _(u'Enter a valid ic.'),
    }
    default_validators = [validators.validate_czechic]

class CzPhoneField(CharField):
    default_error_messages = {
        'invalid': _(u'Enter a valid phone in form +XXX XXXXXXXXX.'),
    }
    default_validators = [validators.validate_czphone]

class CzPostalCodeField(CharField):
    default_error_messages = {
        'invalid': _(u'Enter a valid czech postal code in form XXX XX or XXXXX.'),
    }
    default_validators = [validators.validate_czpostalcode]
    
