'''
Created on 5.12.2011

@author: xaralis
'''
from django.conf.urls.defaults import patterns

class DividedAdmin(object):
    part_classes = ()
    
    @property
    def parts(self):
        if not hasattr(self, '__parts'):
            self.__parts = [p(self) for p in self.part_classes]
        return self.__parts
    
    def get_part_urls(self):
        part_urls = patterns('',)
        for p in self.parts:
            part_urls += p.get_urls()
        return part_urls
        

class AdminPart(object):
    """
    Simple organization part for better ModelAdmin readability.
    """
    def __init__(self, base_admin):
        self.base_admin = base_admin
    
    def admin_view(self, view, cacheable=False):
        return self.base_admin.admin_site.admin_view(view, cacheable)
    
    def get_urls(self):
        return patterns('',)
