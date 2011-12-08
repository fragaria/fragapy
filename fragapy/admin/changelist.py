'''
Created on 1.12.2011

@author: xaralis
'''
from django.contrib.admin.views.main import ChangeList

class SpecialOrderingChangeList(ChangeList):
    def apply_special_ordering(self, queryset):
        order_type, order_by = [self.params.get(param, None) for param in ('ot', 'o')]
        
        ordering_attr = self.model_admin.ordering or self.model._meta.ordering
        
        if order_type is None and order_by is None and ordering_attr is not None:
            order_type = 'desc' if ordering_attr[0] == '-' else 'asc'
            order_by = self.model_admin.list_display.index(ordering_attr[0])
        
        special_ordering = self.model_admin.special_ordering
        if special_ordering and order_type and order_by:
            try:
                order_field = self.list_display[int(order_by)]
                ordering = special_ordering[order_field]
                if order_type == 'desc':
                    ordering = ['-' + field for field in ordering]
                queryset = queryset.order_by(*ordering)
            except IndexError:
                return queryset
            except KeyError:
                return queryset
        return queryset

    def get_query_set(self):
        queryset = super(SpecialOrderingChangeList, self).get_query_set()
        queryset = self.apply_special_ordering(queryset)
        return queryset
