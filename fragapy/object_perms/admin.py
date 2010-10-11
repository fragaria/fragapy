'''
Created on 8.10.2010

@author: xaralis
'''

from django.contrib.contenttypes.generic import GenericTabularInline

from models import ObjectPermission

class ObjectPermissionInline(GenericTabularInline):
    model = ObjectPermission
    raw_id_fields = ['user']

class ObjectPermissionMixin(object):
    def has_change_permission(self, request, obj=None):
        opts = self.opts
        return request.user.has_perm(opts.app_label + '.' 
            + opts.get_change_permission(), obj)

    def has_delete_permission(self, request, obj=None):
        opts = self.opts
        return request.user.has_perm(opts.app_label + '.' 
            + opts.get_delete_permission(), obj)
        
class ObjectPermissionLimitViewMixin(object):
    def queryset(self, request):
        """
        Limit records to only those that the user is authorized to see
        """
        user = request.user
        qs = self.model._default_manager.get_query_set().filter(
            pk__in=[o.pk for o in self.model._default_manager.all() if user.has_perm('view', o)])
        return qs