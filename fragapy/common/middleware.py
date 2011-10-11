from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.html import strip_spaces_between_tags as short


class SpacelessMiddleware(object):
    def process_response(self, request, response):
        if 'text/html' in response['Content-Type']:
            response.content = short(response.content)
        return response
        
        
@staff_member_required
def require_login(request, view_func, view_args, view_kwargs):
    return None

class PermissionMiddleware(object):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.META['REMOTE_ADDR'] not in getattr(settings, 'INTERNAL_IPS', ()):
            return require_login(request, view_func, view_args, view_kwargs)
        return None
        

