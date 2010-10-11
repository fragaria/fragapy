'''
Created on 16.9.2010

@author: xaralis
'''

from django.utils.translation import gettext_lazy as _

class NonDeletableObjectException(Exception):
    def __init__(self, obj):
        self.obj = obj
        
    def __str__(self):
        return _('%s object is marked as non-deletable.' % self.obj) 