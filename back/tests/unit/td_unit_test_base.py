import unittest
from td_types import ImportedTables
from util import db_util

class TdUnitTestBase(unittest.TestCase):    
    def __init__(self,*args, **kwargs):
        super(TdUnitTestBase, self).__init__(*args, **kwargs)
        self.db_handle = db_util.create_db_handle_no_app()        
        self.tables = ImportedTables(self.db_handle)        

    def create_division_final_players(self,num_final_players=2):
        players=[]
        division_final_players = []
        for num in range(1,num_final_players+1):
            players.append(self.create_player(player_id=num))
            division_final_players.append(self.tables.DivisionFinalPlayer(
                final_player_id=num,
                division_final_id=1,
                player_id=num,
                adjusted_seed=num,
                initial_seed=num,
                overall_rank=num            
            ))
            division_final_players[num-1].player=players[num-1]
        return division_final_players
        
    def create_division_final(self,use_division_final_players=True):
        tournament = self.create_single_division_tournament()
        division_final = self.tables.DivisionFinal(
            division_final_id=1,
            division_id=1,            
        )
        division_final.division=tournament.divisions[0]
        
        if use_division_final_players:
            division_final.qualifiers=self.create_division_final_players()
        return division_final
    
    def create_entry(self):
        self.db_handle = db_util.create_db_handle_no_app()        
        self.tables = ImportedTables(self.db_handle)

        self.entry = self.tables.Entry(
            entry_id=1,
            player_id=1,
            division_id=1            
        )            
        self.score = self.tables.Score(
            score_id=1,
            score=12345,
            entry_id=1,
            division_machine_id=1            
        )
        if hasattr(self,'division_machine'):
            self.score.division_machine=self.division_machine
            
        self.entry.scores=[self.score]
        
    def create_queue(self):
        self.db_handle = db_util.create_db_handle_no_app()        
        self.tables = ImportedTables(self.db_handle)
        self.child_queue = self.tables.Queue(
            queue_id=1,
            bumped=False,
            division_machine_id=1,
            parent_id=1,
            queue_child=[],
            division_machine=self.division_machine                        
        )
        self.queue = self.tables.Queue(
            queue_id=2,
            bumped=False,
            division_machine_id=1,
            queue_child=[self.child_queue],
            division_machine=self.division_machine
        )        
        if hasattr(self,'division_machine'):
            self.division_machine.queue = self.queue
            
    def create_division_machine(self):
        self.db_handle = db_util.create_db_handle_no_app()        
        self.tables = ImportedTables(self.db_handle)

        self.machine = self.tables.Machine(
            machine_name='test_machine',
            abbreviation='AAA'
        )        
        self.division_machine = self.tables.DivisionMachine(
            division_machine_id=1,
            removed=False,
            machine_id=self.machine.machine_id,
            division_id=self.division.division_id,
            player_id=1,
            team_id=1
        )
        self.division_machine.machine = self.machine
                
    def create_player(self,player_id=1):
        player = self.tables.Player(
            player_id=player_id,
            first_name="test",
            last_name="player %s" % player_id            
        )
        if hasattr(self,"division_machine"):
            player.division_machine=self.division_machine            
            self.division_machine.player = player
        if hasattr(self,"role"):
            player.roles=[self.role]
        if hasattr(self,"division"):
            player.linked_division_id=self.division.division_id
            player.linked_division=self.division
        return player

    def create_role(self,role_name=None):
        self.db_handle = db_util.create_db_handle_no_app()        
        self.tables = ImportedTables(self.db_handle)
        role = self.tables.Role()
        role.name = role_name
        role.role_id = 1
        return role
    
    
    def create_team(self, team_name=None):
        self.db_handle = db_util.create_db_handle_no_app()        
        self.tables = ImportedTables(self.db_handle)
        if team_name is None:
            team_name='test_test'
        self.team = self.tables.Team(
            team_name=team_name,
            players=[self.player],
            team_id=1
        )        
        if hasattr(self,"division_machine"):
            self.division_machine.team = self.team
        
    def create_audit_log(self):
        self.db_handle = db_util.create_db_handle_no_app()        
        self.tables = ImportedTables(self.db_handle)
        self.create_division_machine()
        self.audit_log = self.tables.AuditLog(
            audit_log_id=1,
            player_id=1,
            entry_id=1,
            token_id=1,
            division_machine_id=1,
            deskworker_id=1,
            scorekeeper_id=1,
            purchase_date=1,
            game_started_date=None,
            used_date=None,
            voided_date=None,
            voided=False,
            used=False,
            remaining_tokens="",
            description="",
            action=""            
        )        
        self.audit_log.division_machine=self.division_machine
        self.audit_log.token=self.token
        
    def create_token(self):
        self.db_handle = db_util.create_db_handle_no_app()        
        self.tables = ImportedTables(self.db_handle)
        self.token = self.tables.Token(
            token_id=1,
            player_id=1,
            division_id=1,
            team_id=1,
            metadivision_id=1,
            paid_for=False,
            used=False
        )        
    def create_multiple_single_div_tournaments(self,tournament_name,num):
        tournaments=[]
        for i in range(num):
            tournament = self.tables.Tournament(
                tournament_id=1,
                tournament_name='%s%s' % (tournament_name,num),
                single_division=True                
            )
            division = self.tables.Division(
                division_id=i,
                division_name='all %s' % num,
                number_of_scores_per_entry=1,                        
                tournament_id=1,
                tournament=tournament,
                active=True
            )
            tournament.divisions=[division]
            tournaments.append(tournament)
        return tournaments
        
    def create_single_division_tournament(self, tournament_name=None):
        self.db_handle = db_util.create_db_handle_no_app()        
        self.tables = ImportedTables(self.db_handle)
        if tournament_name is None:
            tournament_name='test_tournament'
        self.tournament = self.tables.Tournament(
            tournament_id=1,
            tournament_name=tournament_name,
            single_division=True
        )
        self.division = self.tables.Division(
            division_id=1,
            division_name='all',
            number_of_scores_per_entry=1,                        
            tournament_id=1,
            tournament=self.tournament,
            active=True
        )
        self.tournament.divisions=[self.division]
        return self.tournament
    def create_multi_division_tournament(self, tournament_name=None):
        self.db_handle = db_util.create_db_handle_no_app()        
        self.tables = ImportedTables(self.db_handle)
        if tournament_name is None:
            tournament_name='test_tournament'
        self.multi_div_tournament = self.tables.Tournament(
            tournament_id=1,
            tournament_name=tournament_name,
            single_division=False
        )
        self.multi_div_tournament_division = self.tables.Division(
            division_id=1,
            division_name='all',
            number_of_scores_per_entry=1,                        
            tournament_id=1,
            tournament=self.multi_div_tournament,
            active=True
        )
        self.multi_div_tournament.divisions=[self.multi_div_tournament_division]
        
