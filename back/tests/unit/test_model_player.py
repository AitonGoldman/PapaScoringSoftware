import unittest
from td_types import ImportedTables
from util import db_util

class ModelPlayerTD(unittest.TestCase):
    def setUp(self):        
        self.db_handle = db_util.create_db_handle_no_app()        
        self.tables = ImportedTables(self.db_handle)
        self.tournament_one = self.tables.Tournament(            
            tournament_name='test_tournament_one',
            single_division=True
        )
        self.division_one = self.tables.Division(
            division_name='one',            
            tournament_id=1,
            division_id=1,
            tournament=self.tournament_one
        )
        self.machine = self.tables.Machine(
            machine_name='test_machine',
            abbreviation='AAA'
        )
        self.division_machine = self.tables.DivisionMachine(
            removed=False,
            machine_id=self.machine.machine_id,
            division_id=self.division_one.division_id,
            division_machine_id=1
        )
        self.division_machine.machine = self.machine

        self.player_with_roles = self.tables.Player(
            first_name='al',
            last_name='thomka',
            email_address='al@al.com',
            ifpa_ranking=123,            
            active=True,
            pin=1234,
            asshole_count=1)
        self.player_with_roles.linked_division=self.division_one
        self.player_with_roles.division_machine=self.division_machine
        self.role = self.tables.Role()
        self.role.name = "player"
        self.role.role_id = 1
        self.player_with_roles.roles=[self.role]                
        self.player_with_roles.player_id=1
        
        
    def test_player_auth(self):
        self.assertTrue(self.player_with_roles.is_authenticated())   
        self.assertTrue(self.player_with_roles.is_active())   
        self.assertFalse(self.player_with_roles.is_anonymous())           
        
    def test_to_dict_simple(self):                 
        simple_dict_with_roles = self.player_with_roles.to_dict_simple()
        for value in self.player_with_roles.__table__.columns:
            key =  str(value)[str(value).index('.')+1:]            
            self.assertTrue(key in simple_dict_with_roles,"oops - did not find %s" % key)        
        self.assertTrue('roles' in simple_dict_with_roles)
        self.assertEquals(len(simple_dict_with_roles['roles']),1)
        self.assertEquals(simple_dict_with_roles['linked_division']['division_id'],1)
        self.assertEquals(simple_dict_with_roles['division_machine']['division_machine_id'],1)
