angular.module('TDApp').config(['$stateProvider', '$urlRouterProvider',function($stateProvider, $urlRouterProvider) {    
    $stateProvider.state('app.results', 
        { 
         cache: false,
 	 url: '/results',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/results/results.html',
 	       controller: 'app.results'
 	     }
 	   }
       }).state('app.results.divisions', 
        { 
         cache: false,
 	 url: '/divisions',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/results/divisions/divisions.html',
 	       controller: 'app.results.divisions'
 	     }
 	   }
       }).state('app.results.division_machines', 
        { 
         cache: false,
 	 url: '/division_machines',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/results/division_machines/division_machines.html',
 	       controller: 'app.results.division_machines'
 	     }
 	   }
       }).state('app.results.players', 
        { 
         cache: false,
 	 url: '/players',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/results/players/players.html',
 	       controller: 'app.results.players'
 	     }
 	   }
       }).state('app.results.divisions.division', 
        { 
         cache: false,
 	 url: '/division/division_id/:division_id/division_name/:division_name',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/results/divisions/division/division.html',
 	       controller: 'app.results.divisions.division'
 	     }
 	   }
       }).state('app.results.division_machines.machines', 
        { 
         cache: false,
 	 url: '/machines/division_id/:division_id',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/results/division_machines/machines/machines.html',
 	       controller: 'app.results.division_machines.machines'
 	     }
 	   }
       }).state('app.results.division_machines.machines.machine', 
        { 
         cache: false,
 	 url: '/machine/division_machine_id/:division_machine_id/division_machine_name/:division_machine_name',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/results/division_machines/machines/machine/machine.html',
 	       controller: 'app.results.division_machines.machines.machine'
 	     }
 	   }
       }).state('app.results.players.player', 
        { 
         cache: false,
 	 url: '/player/player_id/:player_id/player_name/:player_name/team_id/:team_id',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/results/players/player/player.html',
 	       controller: 'app.results.players.player'
 	     }
 	   }
       }).state('app.results.players.player.team', 
        { 
         cache: false,
 	 url: '/team/team_id/:team_id',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/results/players/player/team/team.html',
 	       controller: 'app.results.players.player.team'
 	     }
 	   }
       }).state('app.results.finals', 
        { 
         cache: false,
 	 url: '/finals',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/results/finals/finals.html',
 	       controller: 'app.results.finals'
 	     }
 	   }
       }).state('app.results.finals.final', 
        { 
         cache: false,
 	 url: '/final/division_final_id/:division_final_id',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/results/finals/final/final.html',
 	       controller: 'app.results.finals.final'
 	     }
 	   }
       }).state('app.results.finals.final.round', 
        { 
         cache: false,
 	 url: '/round/count/:count/round_idx/:round_idx',
 	 views: {
 	     'round_tab@app.results.finals.final': {
 	       templateUrl: 'js/app/results/finals/final/round/round.html',
 	       controller: 'app.results.finals.final.round'
 	     }
 	   }
       }).state('app.results.finals.final.intro', 
        { 
         cache: false,
 	 url: '/round/count/:count/intro',
 	 views: {
 	     'round_tab@app.results.finals.final': {
 	       templateUrl: 'js/app/results/finals/final/intro.html'
 	       //controller: 'app.results.finals.final.round'
 	     }
 	   }
       }).state('app.results.finals.final.round.match_details', 
        { 
         cache: false,
 	 url: '/match_details/division_final_match_idx/:division_final_match_idx/division_final_match_id/:division_final_match_id',
 	 views: {
 	     'round_tab@app.results.finals.final': {
 	       templateUrl: 'js/app/results/finals/final/round/match_details/match_details.html',
 	       controller: 'app.results.finals.final.round.match_details'
 	     }
 	   }
       })//REPLACE_ME













}]);
