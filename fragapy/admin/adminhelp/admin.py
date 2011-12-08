# Copyright (c) 2010 Guilherme Gondim and contributors
#
# This file is part of Django Admin Help.
#
# Django Admin Help is free software under terms of the GNU Lesser
# General Public License version 3 (LGPLv3) as published by the Free
# Software Foundation. See the file README for copying conditions.

from django.contrib import admin
from fragapy.admin.adminhelp.models import HelpPage, Topic

class HelpPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'path', 'topic', 'position')
    list_filter  = ('topic',)
    save_as = True

class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'position')

admin.site.register(HelpPage, HelpPageAdmin)
admin.site.register(Topic, TopicAdmin)
