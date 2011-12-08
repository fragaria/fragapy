'''
Created on 1.12.2011

@author: xaralis
'''
import sys
from string import rfind

from django.utils.importlib import import_module
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

def import_object(module_string):
    # resolve module path and module name
    module_obj_pos = rfind(module_string, '.')
    module_path, module_obj = module_string[:module_obj_pos], module_string[module_obj_pos + 1:] 
    
    # load algorithm dynamically
    module = __import__(module_path, globals(), locals(),
        [module_obj,])
    cls = getattr(module, module_obj)
    
    return cls

def autodiscover_app_modules(modules=()):
    """
    I have copy/pasted this code too many times...Dynamically autodiscover a
    particular module_name in a django project's INSTALLED_APPS directories,
    a-la django admin's autodiscover() method.
    
    Usage:
        autodiscover_app_modules(('commands',)) <-- find all commands.py and load 'em
        
    Credit goes to http://djangosnippets.org/snippets/2404/
    """
    import imp
    
    
    for module_name in modules:
        for app in settings.INSTALLED_APPS:
            try:
                import_module(app)
                app_path = sys.modules[app].__path__
            except AttributeError:
                continue
            try:
                imp.find_module(module_name, app_path)
            except ImportError:
                continue
            import_module('%s.%s' % (app, module_name))
            try:
                app_path = sys.modules['%s.%s' % (app, module_name)]
            except KeyError:
                raise ImproperlyConfigured('Cannot import %s.%s, check for '
                    'import errors.' % (app, module_name))
        