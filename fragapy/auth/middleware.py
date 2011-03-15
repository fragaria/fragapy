from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden
from django.template import RequestContext,Template,loader,TemplateDoesNotExist
from django.utils.importlib import import_module

class PermissionDeniedMiddleware(object):
    def process_exception(self, request, exception):
        if not isinstance(exception, PermissionDenied):
            # Return None so django doesn't re-raise the exception
            return None

        try:
            # Handle import error but allow any type error from view
            callback = getattr(import_module(settings.ROOT_URLCONF), 'handler403')
            return callback(request, exception)
        except (ImportError, AttributeError):
            # Try to get a 403 template
            try:
                # First look for a user-defined template named "403.html"
                t = loader.get_template('403.html')
            except TemplateDoesNotExist:
                print "te"
                # If a template doesn't exist in the projct, use the following hardcoded template
                t = Template("""{% load i18n %}
                 <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"
                        "http://www.w3.org/TR/html4/strict.dtd">
                 <html>
                 <head>
                     <title>{% trans "403 ERROR: Access denied" %}</title>
                 </head>
                 <body>
                     <h1>{% trans "Access Denied (403)" %}</h1>
                     {% trans "We're sorry, but you are not authorized to view this page." %}
                 </body>
                 </html>""")

            # Now use context and render template
            c = RequestContext(request, {'exception': exception})
            return HttpResponseForbidden(t.render(c))
