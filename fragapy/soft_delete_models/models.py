'''
Created on 20.9.2010

@author: xaralis
'''

from django.db import models
from django.utils.translation import ugettext_lazy as _

from managers import SoftDeleteManager

class SoftDeleteableModel(models.Model):
    """
    Replaces hard delete by soft-delete. Object is marked as non-active
    instead of deleting from database.
    """
    active = models.BooleanField(default=True, verbose_name=_('Active'))
    
    objects = SoftDeleteManager()
    
    class Meta:
        abstract = True
        
    def delete(self, using=None):
        self.active = False
        self.save()
        
    def purge(self, using=None):
        self.delete(using)
