'''
Created on 10.8.2011

@author: xaralis
'''
from django.contrib.sites.models import Site
from django.conf import settings

def current_site(request):
    """
    A context processor to add the ``current_site`` to the current Context.
    """
    try:
        current_site = Site.objects.get_current()
        return {
            'current_site': current_site,
        }
    except Site.DoesNotExist:
        return {'current_site': ''} # an empty string


def static(request):
    """
    Adds ``STATIC_URL`` to template context. Beneficial for pre-1.3 Django.
    """
    return {
        'STATIC_URL': getattr(settings, 'STATIC_URL', settings.MEDIA_URL)
    }
