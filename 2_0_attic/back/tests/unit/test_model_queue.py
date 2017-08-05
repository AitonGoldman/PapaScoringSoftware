import unittest
from td_types import ImportedTables
from util import db_util
from td_unit_test_base import TdUnitTestBase

class ModelQueueTD(TdUnitTestBase):
    def setUp(self):        
        self.db_handle = db_util.create_db_handle_no_app()        
        self.tables = ImportedTables(self.db_handle)
        self.create_single_division_tournament()
        self.create_division_machine()
        self.player = self.create_player(1)
        self.player_two = self.create_player(2)        
        self.create_team()        
        self.create_queue()
        self.queue.player_id=1
        self.queue.player=self.player
        self.child_queue.player_id=1
        self.child_queue.player=self.player
    def test_to_dict_simple(self):                 
        simple_dict = self.child_queue.to_dict_simple()
        for value in self.child_queue.__table__.columns:
            key =  str(value)[str(value).index('.')+1:]            
            self.assertTrue(key in simple_dict,"oops - did not find %s" % key)        
        self.assertEquals(simple_dict['division_machine']['division_machine_id'],1)
        self.assertEquals(simple_dict['player']['player_id'],1)        
        self.assertEquals(simple_dict['queue_position'],2)        
 
        
        
