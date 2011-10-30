'''
Created on 28.10.2011

@author: xaralis
'''
from django.db import models

class AdminLinkMixin(object):
    @models.permalink
    def get_admin_url(self):
        return ('admin:%s_%s_change' % (self._meta.app_label, self._meta.object_name.lower()), (self.pk,))