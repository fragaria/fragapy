from datetime import datetime

from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.utils import simplejson as json

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
                    
try:
    # if south support is active, register new fields
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^fragapy\.fields\.models"])
except ImportError:
    pass
