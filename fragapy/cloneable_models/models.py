'''
Created on 20.9.2010

@author: xaralis
'''
from django.db import models

import copy

class Cloneable(models.Model):
    class Meta:
        abstract = True
    
    def clone(self, **kwargs):
        """Return an identical copy of the instance with a new ID."""
        if not self.pk:
            raise ValueError('Instance must be saved before it can be cloned.')

        duplicate = copy.copy(self)

        for attr_name, val in kwargs.items():
            if hasattr(duplicate, attr_name):
               setattr(duplicate, attr_name, val)

        # Setting pk to None tricks Django into thinking this is a new object.
        duplicate.pk = None
        duplicate.id = None
        duplicate.save()

        # ... but the trick loses all ManyToMany relations.
        for field in self._meta.many_to_many:
            source = getattr(self, field.attname)
            destination = getattr(duplicate, field.attname)
            for item in source.all():
                destination.add(item)
        return duplicate

