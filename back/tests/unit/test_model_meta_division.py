import unittest
from td_types import ImportedTables
from util import db_util

class ModelDivisionMachineTD(unittest.TestCase):
    def setUp(self):        
        self.db_handle = db_util.create_db_handle_no_app()        
        self.tables = ImportedTables(self.db_handle)
        self.tournament_one = self.tables.Tournament(            
            tournament_name='test_tournament_one',
            single_division=True
        )
        self.tournament_two = self.tables.Tournament(            
            tournament_name='test_tournament_two',
            single_division=True
        )        
        self.division_one = self.tables.Division(
            division_name='one',            
            tournament_id=1,
            division_id=1,
            tournament=self.tournament_one
        )
        self.division_two = self.tables.Division(
            division_name='one',            
            tournament_id=2,
            division_id=2,
            tournament=self.tournament_two
        )
        self.meta_division = self.tables.MetaDivision(
            meta_division_name='test_meta_division'
        )
        self.meta_division.divisions = [self.division_one,self.division_two]        
        self.meta_division_dict = {'meta_division_name':'test_meta_division',
                                   'meta_division_id':'1',
                                   'division_id':'1',                                      
                                   'removed':False,
                                   'division_machine_id':'1',
                                   'divisions':[
                                       {'division_id':'1'},
                                       {'division_id':'2'}
                                   ]
        }
    
            
    def test_to_dict_simple(self):
        for value in self.meta_division.__table__.columns:
            key =  str(value)[str(value).index('.')+1:]            
            self.assertTrue(key in self.meta_division_dict,"did not find %s"%key)        
    
        returned_meta_division_dict = self.meta_division.to_dict_simple()        
        self.assertEquals(returned_meta_division_dict['divisions'][1]['division_id'],1)
        self.assertEquals(returned_meta_division_dict['divisions'][2]['division_id'],2)
