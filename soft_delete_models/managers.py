'''
Created on 22.9.2010

@author: xaralis
'''

from django.db import models

class SoftDeleteManager(models.Manager):
    def get_query_set(self):
        return super(SoftDeleteManager, self).get_query_set().filter(active=True)
    
    def with_deleted(self):
        return super(SoftDeleteManager, self).get_query_set()