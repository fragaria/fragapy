# Copyright (c) 2010 Guilherme Gondim and contributors
#
# This file is part of Django Admin Help.
#
# Django Admin Help is free software under terms of the GNU Lesser
# General Public License version 3 (LGPLv3) as published by the Free
# Software Foundation. See the file README for copying conditions.

from django import http
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, render_to_response
from django.template import Context, RequestContext, loader
from adminhelp.models import HelpPage

def page_not_found(request, template_name='adminhelp/404.html'):
    """
    Page 404 handler.

    Templates: `adminhelp/404.html`
    Context:
        request_path
            The path of the requested URL (e.g., '/admin/help/app/bad_page/')
        request_help_page_path
            The relative path of the requested help page (e.g., 'app/bad_page/')
    """
    t = loader.get_template(template_name)
    context = {
        'request_path': request.path,
        'request_help_page_path': '/'.join(request.path.split('/')[3:])
    }
    return http.HttpResponseNotFound(t.render(RequestContext(request, context)))

def help_index(request, path=None, template_name='adminhelp/index.html'):
    """
    Templates: `adminhelp/index.html`
    Context:
        page_list
            A QuerySet with all help pages, useful to generate a index or menu.
    """
    context = {'page_list':  HelpPage.objects.all()}
    return render_to_response(template_name, context,
                              context_instance=RequestContext(request))
help_index = staff_member_required(help_index)

def help_page(request, id, template_name='adminhelp/help_page.html'):
    """
    Templates: `adminhelp/page.html`
    Context:
        page
            A HelpPage object matching to `path`.
        page_list
            A QuerySet with all help pages, useful to generate a index or menu.
    """
    try:
        help_page = HelpPage.objects.get(id=id)
    except HelpPage.DoesNotExist:
        return page_not_found(request)
    context = {'page': help_page, 'page_list': HelpPage.objects.all()}
    return render_to_response(template_name, context,
                              context_instance=RequestContext(request))
help_page = staff_member_required(help_page)
