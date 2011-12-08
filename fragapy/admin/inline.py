'''
Created on 1.12.2011

@author: xaralis
'''
from django.contrib import admin
from django.db.models.fields import AutoField

class NonEditableInline(admin.TabularInline):
    """
    Usefull class if we need non-editable inline.
    Only readonly without add, edit or delete action
    """
    def __init__(self, parent_model, admin_site):
        super(NonEditableInline, self).__init__(parent_model, admin_site)                
        self.readonly_fields = [field.name for field in self.model._meta.fields if not isinstance(field, AutoField)]
        self.can_delete = False
        self.max_num = 0
        self.extra = 0
        
    class Media:
        css = {
            "all": ("admin/css/non_editable_inline.css",)
        }