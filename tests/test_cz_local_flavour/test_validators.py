'''
Created on 21.9.2010

@author: xaralis
'''
from django.forms import ValidationError

from nose.tools import raises
from djangosanetesting.cases import UnitTestCase

from fragapy.cz_localflavour.validators import validate_czechic, \
    validate_czphone, validate_czpostalcode

class TestValidateCzechIc(UnitTestCase):
    def setUp(self):
        super(TestValidateCzechIc, self).setUp()
        self.func = validate_czechic
    
    def test_succeed_for_correct_forms(self):
        self.assert_equals(self.func('48590151'), None)
        self.assert_equals(self.func('25717421'), None)
        self.assert_equals(self.func('71232222'), None)
        
    @raises(ValidationError)
    def test_fail_for_incorrect_form(self):
        self.func('71232221')
        
    @raises(ValidationError)
    def test_fail_when_too_small(self):
        self.func('123')
    
    @raises(ValidationError)
    def test_fail_when_too_long(self):
        self.func('71232221123123')

class TestValidateCzechPhone(UnitTestCase):
    def setUp(self):
        super(TestValidateCzechPhone, self).setUp()
        self.func = validate_czphone
        
    def test_succeed_for_correct_forms(self):
        self.assert_equals(self.func('+420123123123'), None)
        self.assert_equals(self.func('+420 123 123 123'), None)
        self.assert_equals(self.func('123 123 123'), None)
        self.assert_equals(self.func('+420-123 123 123'), None)
        self.assert_equals(self.func('+420 123123123'), None)
        self.assert_equals(self.func('123123123'), None)
        
    @raises(ValidationError)
    def test_fail_for_letters(self):
        self.func('+a')
        
    @raises(ValidationError)
    def test_fail_when_too_small(self):
        self.func('+420')
    
    @raises(ValidationError)
    def test_fail_when_too_long(self):
        self.func('+4201234567890123456')
        
    @raises(ValidationError)
    def test_fail_when_unsuitable_chars_are_found(self):
        self.func('+420_123123123')
        
class TestValidateCzechPostalCode(UnitTestCase):
    def setUp(self):
        super(TestValidateCzechPostalCode, self).setUp()
        self.func = validate_czpostalcode
        
    def test_succeed_for_correct_forms(self):
        self.assert_equals(self.func('130 00'), None)
        self.assert_equals(self.func('13000'), None)
        
    @raises(ValidationError)
    def test_fail_for_letters(self):
        self.func('13a 00')
        
    @raises(ValidationError)
    def test_fail_when_too_small(self):
        self.func('130')
    
    @raises(ValidationError)
    def test_fail_when_too_long(self):
        self.func('130000')
