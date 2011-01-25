from django.forms import CharField, ValidationError
from django.utils import simplejson

from widgets import DictionaryInputs

class DictionaryField(CharField):
    """
    Utility field that doesn't convert returned value from widget to string.
    It keeps it as dictionary instead.    
    """
    widget = DictionaryInputs
    
    def clean(self, value):
        if not isinstance(value, dict):
            raise ValidationError(self.error_messages['invalid'])
        return value

class JSONField(CharField):
    def __init__(self, *args, **kwargs):
        super(JSONField, self).__init__(*args, **kwargs)

    def clean(self, value):
        value = super(JSONField, self).clean(value)
        try:
            json_data = simplejson.loads(value)
        except Exception, e:
            raise ValidationError(self.error_messages['invalid'])
        return json_data
