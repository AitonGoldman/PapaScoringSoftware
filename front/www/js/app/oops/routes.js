angular.module('TDApp').config(['$stateProvider', '$urlRouterProvider',function($stateProvider, $urlRouterProvider) {    
    $stateProvider.state('app.oops', 
        { 
         cache: false,
 	 url: '/oops',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/oops/oops.html',
 	       controller: 'app.oops'
 	     }
 	   }
       }).state('app.oops.edit_player_entries', 
        { 
         cache: false,
 	 url: '/edit_player_entries',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/oops/edit_player_entries/edit_player_entries.html',
 	       controller: 'app.oops.edit_player_entries'
 	     }
 	   }
       }).state('app.oops.edit_player_entries.player_entries', 
        { 
         cache: false,
 	 url: '/player_entries/player_id/:player_id/new_division_machine_id/:new_division_machine_id/new_division_machine_name/:new_division_machine_name',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/oops/edit_player_entries/player_entries/player_entries.html',
 	       controller: 'app.oops.edit_player_entries.player_entries'
 	     }
 	   }
       }).state('app.oops.edit_player_entries.player_entries.select_division_machine', 
        { 
         cache: false,
 	 url: '/select_division_machine/player_id/:player_id',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/oops/edit_player_entries/player_entries/select_division_machine/select_division_machine.html',
 	       controller: 'app.oops.edit_player_entries.player_entries.select_division_machine'
 	     }
 	   }
       }).state('app.oops.missing_tokens', 
        { 
         cache: false,
 	 url: '/missing_tokens',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/oops/missing_tokens/missing_tokens.html',
 	       controller: 'app.oops.missing_tokens'
 	     }
 	   }
       }).state('app.oops.missing_tokens.report', 
        { 
         cache: false,
 	 url: '/report/player_id/:player_id',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/oops/missing_tokens/report/report.html',
 	       controller: 'app.oops.missing_tokens.report'
 	     }
 	   }
       })//REPLACE_ME






}]);
