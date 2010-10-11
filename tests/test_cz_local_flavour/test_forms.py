'''
Created on 21.9.2010

@author: xaralis
'''
from django.forms import ValidationError

from nose.tools import raises
from djangosanetesting.cases import UnitTestCase

from fragapy.cz_localflavour.forms import CzPhoneField, CzPostalCodeField

class TestCzPhoneField(UnitTestCase):
    def setUp(self):
        super(TestCzPhoneField, self).setUp()
        self.field = CzPhoneField()
    
    def test_succeed_for_correct_forms(self):
        self.assert_equals('+420123123123', self.field.clean('+420123123123'))
        self.assert_equals('+420 123 123 123', self.field.clean('+420 123 123 123'))
        self.assert_equals('123 123 123', self.field.clean('123 123 123'))
        self.assert_equals('+420-123 123 123', self.field.clean('+420-123 123 123'))
        self.assert_equals('+420 123123123', self.field.clean('+420 123123123'))
        self.assert_equals('123123123', self.field.clean('123123123'))
        
    @raises(ValidationError)
    def test_fail_for_letters(self):
        self.field.clean('+a')
        
    @raises(ValidationError)
    def test_fail_when_too_small(self):
        self.field.clean('+420')
    
    @raises(ValidationError)
    def test_fail_when_too_long(self):
        self.field.clean('+4201234567890123456')
        
    @raises(ValidationError)
    def test_fail_when_unsuitable_chars_are_found(self):
        self.field.clean('+420_123123123')
        
class TestCzPostalCodeField(UnitTestCase):
    def setUp(self):
        super(TestCzPostalCodeField, self).setUp()
        self.field = CzPostalCodeField()
    
    def test_succeed_for_correct_forms(self):
        self.assert_equals('13000', self.field.clean('13000'))
        self.assert_equals('130 00', self.field.clean('130 00'))
        
    @raises(ValidationError)
    def test_fail_for_letters(self):
        self.field.clean('13a 00')
        
    @raises(ValidationError)
    def test_fail_when_too_small(self):
        self.field.clean('130')
        
    @raises(ValidationError)
    def test_fail_when_too_long(self):
        self.field.clean('130000')
