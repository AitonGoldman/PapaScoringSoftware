import unittest
from td_types import ImportedTables
from util import db_util

class ModelQueueTD(unittest.TestCase):
    def setUp(self):        
        self.db_handle = db_util.create_db_handle_no_app()        
        self.tables = ImportedTables(self.db_handle)
        self.machine = self.tables.Machine(
            machine_name='test_machine',
            abbreviation='AAA'
        )
        self.division_machine = self.tables.DivisionMachine(
            removed=False,
            machine_id=self.machine.machine_id,            
            division_machine_id=1
        )
        self.division_machine.machine = self.machine
        self.player_1 = self.tables.Player(
            first_name='al',
            last_name='thomka',
            player_id=1)
        self.player_2 = self.tables.Player(
            first_name='al',
            last_name='thomka2',
            player_id=2)
        self.player_3 = self.tables.Player(
            first_name='al',
            last_name='thomka3',
            player_id=3)
        self.player_4 = self.tables.Player(
            first_name='al',
            last_name='thomka4',
            player_id=4)
        self.queue_root = self.tables.Queue(
            queue_id=1,
            player_id=1,
            division_machine_id=1,
            division_machine=self.division_machine,
            player=self.player_1
        )
        self.queue_second = self.tables.Queue(
            queue_id=2,
            player_id=2,
            division_machine_id=1,
            division_machine=self.division_machine,
            player=self.player_2
        )
        self.queue_root.queue_child = [self.queue_second]
        self.division_machine.queue = self.queue_root

    def test_to_dict_simple(self):                 
        simple_dict = self.queue_second.to_dict_simple()
        for value in self.queue_root.__table__.columns:
            key =  str(value)[str(value).index('.')+1:]            
            self.assertTrue(key in simple_dict,"oops - did not find %s" % key)        
        self.assertEquals(simple_dict['division_machine']['division_machine_id'],1)
        self.assertEquals(simple_dict['player']['player_id'],2)        
        self.assertEquals(simple_dict['queue_position'],2)        
 
        
        
