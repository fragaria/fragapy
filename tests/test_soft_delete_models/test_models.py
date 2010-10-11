'''
Created on 21.9.2010

@author: xaralis
'''
from djangosanetesting.cases import DatabaseTestCase

from testapp.models import DummySoftDeletableModel

class TestSoftDeleteableModel(DatabaseTestCase):
    def setUp(self):
        super(TestSoftDeleteableModel, self).setUp()
        self.obj, self.created = DummySoftDeletableModel.objects.get_or_create(pk=1)
        
    def test_not_active_after_delete(self):
        self.assert_equals(self.obj.active, True)
        self.obj.delete()
        self.assert_equals(self.obj.active, False)
        
    def test_in_db_after_delete(self):
        pk = self.obj.pk
        self.obj.delete()
        DummySoftDeletableModel.objects.with_deleted().get(pk=pk)