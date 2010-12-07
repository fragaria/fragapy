# Copyright (c) 2010 Guilherme Gondim and contributors
#
# This file is part of Django Admin Help.
#
# Django Admin Help is free software under terms of the GNU Lesser
# General Public License version 3 (LGPLv3) as published by the Free
# Software Foundation. See the file README for copying conditions.

from django.conf.urls.defaults import *
from adminhelp.views import help_index, help_page

help_index_url = url(
    regex=r'^$',
    view=help_index,
    name='help_index',
)

help_page_url = url(
    regex=r'^(?P<id>\d+)/$',
    view=help_page,
    name='help_page',
)

urlpatterns = patterns('', help_index_url, help_page_url)
