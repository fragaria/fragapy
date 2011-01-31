from datetime import datetime

from django import forms
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.utils import simplejson as json
from django.utils.text import capfirst


import fields

class JSONField(models.TextField):
    """
    JSONField is a generic textfield that neatly serializes/unserializes
    JSON objects seamlessly
    """
    # Used so to_python() is called
    __metaclass__ = models.SubfieldBase
    
    def to_python(self, value):
        """Convert our string value to JSON after we load it from the DB"""
    
        if value == "":
            return None
    
        try:
            if isinstance(value, basestring):
                return json.loads(value)
        except ValueError:
            pass
    
        return value
                    
    def get_prep_value(self, value):
        """
        Convert our JSON object to a string before we save
        """
        if value == "":
            return None
        if isinstance(value, dict) or isinstance(value, dict):
            value = json.dumps(value, cls=DjangoJSONEncoder)
        return super(JSONField, self).get_prep_value(value)
                    
    def value_to_string(self, obj):
        """
        called by the serializer.
        """
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)

class MultiSelectField(models.Field):
    __metaclass__ = models.SubfieldBase

    def get_internal_type(self):
        return "CharField"

    def get_choices_default(self):
        return self.get_choices(include_blank=False)

    def _get_FIELD_display(self, field):
        value = getattr(self, field.attname)
        choicedict = dict(field.choices)

    def formfield(self, **kwargs):
        # don't call super, as that overrides default widget if it has choices
        defaults = {'required': not self.blank, 'label': capfirst(self.verbose_name), 
                    'help_text': self.help_text, 'choices':self.choices}
        if self.has_default():
            defaults['initial'] = self.get_default()
        defaults.update(kwargs)
        return fields.MultiSelectFormField(**defaults)

    def get_db_prep_value(self, value):
        if isinstance(value, basestring):
            return value
        elif isinstance(value, list):
            return ",".join(value)

    def to_python(self, value):
        if isinstance(value, list):
            return value
        elif value == None:
            return None
        return value.split(",")
    
    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)

    def contribute_to_class(self, cls, name):
        super(MultiSelectField, self).contribute_to_class(cls, name)
        if self.choices:
            def display_func(self, fieldname=name, choicedict=dict(self.choices)):
                vals = getattr(self, fieldname)
                if vals is not None:
                    return ", ".join([choicedict.get(value, value) for value in vals])
                return None 
            setattr(cls, 'get_%s_display' % self.name, display_func)
            
    def validate(self, value, model_instance): 
        return

try:
    # if south support is active, register new fields
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^fragapy\.fields\.models"])
except ImportError:
    pass
