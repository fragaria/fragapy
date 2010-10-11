'''
Created on 8.10.2010

@author: xaralis
'''
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _

BASE_USER_CLASS = getattr(settings, 'BASE_USER_CLASS', 'User')

class ObjectPermission(models.Model):
    user = models.ForeignKey(BASE_USER_CLASS)
    can_view = models.BooleanField()
    can_change = models.BooleanField()
    can_delete = models.BooleanField()

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    
    class Meta:
        verbose_name = _('Object permission')
        verbose_name_plural = _('Object permissions')
        
    def __unicode__(self):
        obj = self.content_type.get_object_for_this_type(pk=self.object_id)
        return _('Permission settings for %s') % unicode(obj)