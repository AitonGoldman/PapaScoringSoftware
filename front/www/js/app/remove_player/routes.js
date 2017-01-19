angular.module('TDApp').config(['$stateProvider', '$urlRouterProvider',function($stateProvider, $urlRouterProvider) {    
    $stateProvider.state('app.remove_player', 
        { 
         cache: false,
 	 url: '/remove_player',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/remove_player/remove_player.html',
 	       controller: 'app.remove_player'
 	     }
 	   }
       }).state('app.remove_player.confirm', 
        { 
         cache: false,
 	 url: '/confirm/player_id/:player_id/player_name/:player_name/machine_name/:machine_name/division_machine_id/:division_machine_id',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/remove_player/confirm/confirm.html',
 	       controller: 'app.remove_player.confirm'
 	     }
 	   }
       }).state('app.remove_player.confirm.process', 
        { 
         cache: false,
 	 url: '/process',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/remove_player/confirm/process/process.html',
 	       controller: 'app.remove_player.confirm.process'
 	     }
 	   }, params: {
             process_step:{}
             
          }    

       })//REPLACE_ME



}]);
