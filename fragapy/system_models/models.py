'''
Created on 16.9.2010

@author: xaralis
'''

from django.db import models
from django.utils.translation import ugettext_lazy as _

from exceptions import NonDeletableObjectException

class SystemModel(models.Model):
    deleteable = models.BooleanField(default=True, editable=False,
        verbose_name=_('Deletable'))
    
    class Meta:
        abstract = True
        
    def delete(self, using=None):
        if not self.deleteable:
            raise NonDeletableObjectException(self)
        super(SystemModel, self).delete(using)
