'''
Created on 16.9.2010

@author: xaralis
'''

import re

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _

class CzechIcValidator(object):
    message = _(u'Enter a valid ic.')
    code = 'invalid'

    def __call__(self, value):
        """
        Validates that the input matches the czech ic number.
        """
        ic_number = re.compile(r'^(?P<number>\d{7})(?P<check>\d)$')
        
        match = re.match(ic_number, value)
        if not match:
            raise ValidationError(self.message)

        number, check = match.groupdict()['number'], int(match.groupdict()['check'])

        sum = 0
        weight = 8
        for digit in number:
            sum += int(digit)*weight
            weight -= 1

        remainder = sum % 11

        # remainder is equal:
        #  0 or 10: last digit is 1
        #  1: last digit is 0
        # in other case, last digin is 11 - remainder

        if (not remainder % 10 and check == 1) or \
        (remainder == 1 and check == 0) or \
        (check == (11 - remainder)):
            return
        else:
            raise ValidationError(self.message, code=self.code)

czphone_re = re.compile(r"^\+\d{3}[- ]?\d{9}$")
validate_czphone = RegexValidator(czphone_re, _('Enter a valid phone in form +XXX XXXXXXXXX.'), 'invalid')

czpostalcode_re = re.compile(r'^\d{5}$|^\d{3} \d{2}$')
validate_czpostalcode = RegexValidator(czpostalcode_re, _('Enter a valid czech postal code in form XXX XX or XXXXX.'), 'invalid')

validate_czechic = CzechIcValidator()
