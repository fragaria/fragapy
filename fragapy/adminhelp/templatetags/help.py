# Copyright (c) 2010 Guilherme Gondim and contributors
#
# This file is part of Django Admin Help.
#
# Django Admin Help is free software under terms of the GNU Lesser
# General Public License version 3 (LGPLv3) as published by the Free
# Software Foundation. See the file README for copying conditions.

from django.template import Library
from fragapy.adminhelp.models import HelpPage

register = Library()

def help_link(context):
    """TODO
    """
    path = '/'.join(context['request'].path.split('/')[2:])
    try:
        help_page_url = HelpPage.objects.get(path=path).get_absolute_url()
    except HelpPage.DoesNotExist:
        help_page_url = None
    return {'help_page_url': help_page_url}

register.inclusion_tag('adminhelp/includes/help_link.html',
                       takes_context=True)(help_link)

def help_list_item(context):
    """TODO
    """
    path = '/'.join(context['request'].path.split('/')[2:])
    try:
        help_page_url = HelpPage.objects.get(path=path).get_absolute_url()
    except HelpPage.DoesNotExist:
        help_page_url = None
    return {'help_page_url': help_page_url}

register.inclusion_tag('adminhelp/includes/help_list_item.html',
                       takes_context=True)(help_list_item)
