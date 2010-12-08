# Copyright (c) 2010 Guilherme Gondim and contributors
#
# This file is part of Django Admin Help.
#
# Django Admin Help is free software under terms of the GNU Lesser
# General Public License version 3 (LGPLv3) as published by the Free
# Software Foundation. See the file README for copying conditions.

from django.db import models
from django.utils.translation import ugettext_lazy as _
import positions

class Topic(models.Model):
    name = models.CharField(_('name'), max_length=64, unique=True, db_index=True)
    position = positions.PositionField(_('position'))

    class Meta:
        ordering = ('position', 'name')
        verbose_name = _('topic')
        verbose_name_plural = _('topics')

    def __unicode__(self):
        return u'%s' % self.name

class HelpPage(models.Model):
    topic = models.ForeignKey(Topic, verbose_name=_('topic'))
    path = models.CharField(
        _('path'),
        max_length=128,
        db_index=True,
        unique=True,
        help_text=('Use paths relative to your admin path '
                   '(<code>/admin/</code>). Examples: '
                   '<code>auth/user/</code>, <code>password_change/</code>, '
                   '<code>myapp/mymodel/</code>.')
    )
    title = models.CharField(_('title'), max_length=128)
    content = models.TextField(_('content'), blank=True)
    position = positions.PositionField(_('position'), collection=('topic',))

    class Meta:
        ordering = ('topic', 'position', 'title')
        verbose_name = _('help page')
        verbose_name_plural = _('help pages')

    def __unicode__(self):
        return u'%s (%s)' % (self.title, self.path)

    def get_absolute_url(self):
        return ('help_page', None, {'id': str(self.id)})
    get_absolute_url = models.permalink(get_absolute_url)
