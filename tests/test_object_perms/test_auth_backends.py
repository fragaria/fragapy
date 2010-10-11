'''
Created on 8.10.2010

@author: xaralis
'''

from django.contrib.contenttypes.models import ContentType

from djangosanetesting.cases import DatabaseTestCase

from fragapy.object_perms.models import ObjectPermission

from tests.apps.helpers import get_user

from testapp.models import DummyPermModel

class TestObjectPermissionBackend(DatabaseTestCase):
    def setUp(self):
        super(TestObjectPermissionBackend, self).setUp()
        self.object, created = DummyPermModel.objects.get_or_create(pk=1)
        self.user = get_user(is_superuser=False)
        
    def test_permissions(self):
        ct = ContentType.objects.get_for_model(self.object.__class__)
        p = ObjectPermission.objects.create(user=self.user, can_view=True,
            can_change=True, can_delete=True, content_type=ct,
            object_id=self.object.pk)
        
        self.assert_true(self.user.has_perm('delete', self.object))
        self.assert_true(self.user.has_perm('change', self.object))
        self.assert_true(self.user.has_perm('view', self.object))
        
        p.can_change = False
        p.save()
        
        self.assert_true(self.user.has_perm('delete', self.object))
        self.assert_false(self.user.has_perm('change', self.object))
        self.assert_true(self.user.has_perm('view', self.object))
        
        p.can_delete = False
        p.save()
        
        self.assert_false(self.user.has_perm('delete', self.object))
        self.assert_false(self.user.has_perm('change', self.object))
        self.assert_true(self.user.has_perm('view', self.object))
        
        p.can_view   = False
        p.save()
        
        self.assert_false(self.user.has_perm('delete', self.object))
        self.assert_false(self.user.has_perm('change', self.object))
        self.assert_false(self.user.has_perm('view', self.object))