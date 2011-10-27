from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.html import strip_spaces_between_tags as short


class SpacelessMiddleware(object):
    """
    Add to ``MIDDLEWARE_CLASSES`` when you want to have all of your HTML reponses
    to be smaller.
    
    Reduces the size of HTML response by applying ``strip_spaces_between_tags``
    always.
    """
    def process_response(self, request, response):
        if 'text/html' in response['Content-Type']:
            response.content = short(response.content)
        return response
        
        
@staff_member_required
def require_login(request, view_func, view_args, view_kwargs):
    return None

class PermissionMiddleware(object):
    """
    Special middleware for sites that should not be seen by general public.
    
    If ``REMOTE_ADDR`` is not in ``INTERNAL_IPS`` setting, login form
    will be displayed and the person would not be let in until it fills the
    form correctly.
    """
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.META['REMOTE_ADDR'] not in getattr(settings, 'INTERNAL_IPS', ()):
            return require_login(request, view_func, view_args, view_kwargs)
        return None
        

