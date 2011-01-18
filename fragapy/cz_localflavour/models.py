'''
Created on 16.9.2010

@author: xaralis
'''

from django.db.models import CharField
from django.utils.translation import gettext_lazy as _

import validators

class CzPhoneField(CharField):
    default_validators = [validators.validate_czphone]
    description = _("Czech phone number")
    
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = kwargs.get('max_length', 30)
        super(CharField, self).__init__(*args, **kwargs)

class CzPostalCodeField(CharField):
    default_validators = [validators.validate_czpostalcode]
    description = _('Czech postal code')
    
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = kwargs.get('max_length', 6)
        super(CharField, self).__init__(*args, **kwargs)
        
class CzechIcField(CharField):
    default_validators = [validators.validate_czechic]
    description = _('Czech ic')
    
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = kwargs.get('max_length', 9)
        super(CharField, self).__init__(*args, **kwargs)
        
try:
    # if south support is active, register new fields
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^fragapy\.cz_localflavour\.models"])
except ImportError:
    pass
