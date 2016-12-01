import unittest
from td_types import ImportedTables
from util import db_util

class ModelDivisionMachineTD(unittest.TestCase):
    def setUp(self):        
        self.db_handle = db_util.create_db_handle_no_app()        
        self.tables = ImportedTables(self.db_handle)
        self.tournament = self.tables.Tournament(            
            tournament_name='test_tournament',
            single_division=True
        )
        self.division = self.tables.Division(
            division_name='a',            
            tournament_id=1,
            tournament=self.tournament
        )
        self.machine = self.tables.Machine(
            machine_name='test_machine',
            abbreviation='AAA'
        )        
        self.division_machine = self.tables.DivisionMachine(
            removed=False,
            machine_id=self.machine.machine_id,
            division_id=self.division.division_id,
            player_id=1,
            team_id=1
        )
        self.player = self.tables.Player(
            player_id=1,
            first_name="test",
            last_name="player",
            division_machine=self.division_machine
        )
        self.team = self.tables.Team(
            team_name='test_test',
            players=[self.player],
            team_id=1
        )        

        self.division_machine.player = self.player
        self.division_machine.machine = self.machine
        self.division_machine.team = self.team
        #self.db_handle.session.add(self.division)
        self.division_machine_dict = {'division_machine_name':'test_machine',
                                      'machine_id':'1',
                                      'division_id':'1',                                      
                                      'removed':False,
                                      'division_machine_id':'1',
                                      'player_id':'1',
                                      'team_id':'1'
        }
    
            
    def test_to_dict_simple(self):
        for value in self.division_machine.__table__.columns:
            key =  str(value)[str(value).index('.')+1:]            
            self.assertTrue(key in self.division_machine_dict,"did not find %s"%key)        
    
        returned_division_machine_dict = self.division_machine.to_dict_simple()
        self.assertEquals(returned_division_machine_dict['division_machine_name'],'test_machine')
        self.assertEquals(returned_division_machine_dict['abbreviation'],'AAA')
        self.assertEquals(returned_division_machine_dict['player']['player_id'],1)
        self.assertEquals(returned_division_machine_dict['team']['team_id'],1)
        
