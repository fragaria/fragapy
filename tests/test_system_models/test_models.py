'''
Created on 21.9.2010

@author: xaralis
'''
from nose.tools import raises
from djangosanetesting.cases import DatabaseTestCase

from fragapy.system_models.exceptions import NonDeletableObjectException

from testapp.models import DummySystemModel

class TestSystemModel(DatabaseTestCase):
    def setUp(self):
        super(TestSystemModel, self).setUp()
        self.obj_system, self.created = DummySystemModel.objects.get_or_create(deleteable=False)
        self.obj_nonsystem, self.created = DummySystemModel.objects.get_or_create(deleteable=True)
        
    @raises(NonDeletableObjectException)
    def test_delete_fails_when_model_not_deletable(self):
        self.obj_system.delete()
        
    def test_delete_passes_when_model_is_deletable(self):
        self.obj_nonsystem.delete()