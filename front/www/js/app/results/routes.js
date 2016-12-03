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
 	 url: '/player/player_id/:player_id/player_name/:player_name',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/results/players/player/player.html',
 	       controller: 'app.results.players.player'
 	     }
 	   }
       })//REPLACE_ME








}]);
