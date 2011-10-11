# Aliasing it for the sake of page size.
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.html import strip_spaces_between_tags as short

class SpacelessMiddleware(object):
    def process_response(self, request, response):
        if 'text/html' in response['Content-Type']:
            response.content = short(response.content)
        return response
        
        

class PermissionMiddleware(object):
    def __init__(self):
        self.process_view = staff_member_required(self.process_view)

    def process_view(self, request, view_func, view_args, view_kwargs):
        return None
