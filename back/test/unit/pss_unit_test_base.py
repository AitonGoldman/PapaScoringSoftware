import unittest
from pss_models import ImportedTables
from lib.DbInfo import DbInfo
from mock import MagicMock
from flask_sqlalchemy import SQLAlchemy

class PssUnitTestBase(unittest.TestCase):    
    def __init__(self,*args, **kwargs):
        super(PssUnitTestBase, self).__init__(*args, **kwargs)                        
        self.db_handle = SQLAlchemy()
        #FIXME : need constants for these strings
        self.tables = ImportedTables(self.db_handle,'test_app','test_pss_amin_app')        
        self.mock_app = MagicMock()

    def create_mock_queues(self):
        self.mock_queue_one=MagicMock()
        self.mock_queue_one.tournament_machine_id=1
        self.mock_queue_one.player_id=1
        self.mock_queue_one.bumped=False
        self.mock_queue_one.position=1
        
        self.mock_queue_two=MagicMock()
        self.mock_queue_two.tournament_machine_id=1
        self.mock_queue_two.player_id=2
        self.mock_queue_two.bumped=False
        self.mock_queue_two.position=2

        self.mock_queue_three=MagicMock()
        self.mock_queue_three.tournament_machine_id=1
        self.mock_queue_three.player_id=3
        self.mock_queue_three.bumped=False
        self.mock_queue_three.position=3

        self.mock_queue_four=MagicMock()        
        self.mock_queue_four.tournament_machine_id=1
        self.mock_queue_four.player_id=None
        self.mock_queue_four.player_id=4
        self.mock_queue_four.bumped=False
        self.mock_queue_four.position=4
        
    def create_mock_role(self,role_name):
        mock_role = MagicMock()
        mock_role.name = role_name
        return mock_role
    
    def create_mock_player(self,role_names):
        mock_player = MagicMock()        
        mock_player.player_roles=[]        
        for role_name in role_names:
            mock_role = self.create_mock_role(role_name)
            mock_player.player_roles.append(mock_role)                        
        return mock_player
    
    def create_mock_user(self,role_names,is_pss_admin_user=True):
        mock_user = MagicMock()        
        mock_user.admin_roles=[]
        mock_user.event_roles=[]
        for role_name in role_names:
            mock_role = self.create_mock_role(role_name)
            if is_pss_admin_user:
                mock_user.admin_roles.append(mock_role)
            else:
                mock_user.event_roles.append(mock_role)
                
        mock_user.verify_password.return_value=True            
        return mock_user

    def generate_side_effect_confirm_args(self,args_to_confirm,values=None,return_value=None,return_count=None):
        def side_effect_confirm_args(*args,**kargs):                        
            for arg_to_confirm in args_to_confirm:                
                if arg_to_confirm not in kargs:
                    raise Exception('args %s not found' % arg_to_confirm)
                if values and arg_to_confirm in values and values[arg_to_confirm]!=kargs[arg_to_confirm]:
                    raise Exception('arg "%s" is expected to be "%s", but instead got "%s"' % (arg_to_confirm, values[arg_to_confirm],kargs[arg_to_confirm]))
                    
            for arg_actually_used in kargs.keys():
                if arg_actually_used not in args_to_confirm:
                    print "\n !!!!!!! found arg %s was used, but was not expecting it\n" % arg_actually_used            
            if return_value:
                return return_value
            elif return_count:                
                count_mock = MagicMock()
                count_mock.count.return_value=return_count
                return count_mock
            else:
                return MagicMock()
        return side_effect_confirm_args
        
    def generate_mock_user_side_effect(self,side_effect_mock_user):
        def return_mock_user(*args,**kargs):            
            mock = MagicMock()
            if len(kargs) == 1:
                mock.first.return_value=None
            else:
                mock.first.return_value=side_effect_mock_user            
            return mock
        return return_mock_user
