from django import forms
from django.contrib.humanize.templatetags.humanize import apnumber
from django.forms import CharField, ValidationError
from django.template.defaultfilters import pluralize

from widgets import DictionaryInputs

try:
	import json
except ImportError:
	from django.utils import simplejson as json


class DictionaryField(CharField):
    """
    Utility field that doesn't convert returned value from widget to string.
    It keeps it as dictionary instead.
    """
    widget = DictionaryInputs

    def __init__(self, value_validators=[], *args, **kwargs):
        self.value_validators = value_validators
        super(DictionaryField, self).__init__(*args, **kwargs)

    def clean(self, value):
        self.validate(value)
        return value

    def validate(self, value):
        self.run_validators(value)
        if not isinstance(value, dict):
            raise ValidationError(self.error_messages['invalid'])
        if self.value_validators:
            for val in value.values():
                for validator in self.value_validators:
                    validator(val)


class JSONField(CharField):
    def __init__(self, *args, **kwargs):
        super(JSONField, self).__init__(*args, **kwargs)

    def clean(self, value):
        value = super(JSONField, self).clean(value)
        try:
            json_data = json.loads(value)
        except Exception, e:
            raise ValidationError(self.error_messages['invalid'])
        return json_data


class MultiSelectFormField(forms.MultipleChoiceField):
    widget = forms.CheckboxSelectMultiple

    def __init__(self, *args, **kwargs):
        self.max_choices = kwargs.pop('max_choices', 0)
        super(MultiSelectFormField, self).__init__(*args, **kwargs)

    def clean(self, value):
        if not value and self.required:
            raise forms.ValidationError(self.error_messages['required'])
        return value
