angular.module('TDApp').config(['$stateProvider', '$urlRouterProvider',function($stateProvider, $urlRouterProvider) {    
    $stateProvider.state('app.queue_player_after_play', 
        { 
         cache: false,
 	 url: '/queue_player_after_play/division_id/:division_id/player_id/:player_id/player_name/:player_name/division_name/:division_name/division_machine_just_played_id/:division_machine_just_played_id/division_machine_just_played_name/:division_machine_just_played_name',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/queue_player_after_play/queue_player_after_play.html',
 	       controller: 'app.queue_player_after_play'
 	     }
 	   }
       }).state('app.queue_player_after_play.confirm', 
        { 
         cache: false,
 	 url: '/confirm/division_machine_to_queue_on_id/:division_machine_to_queue_on_id/division_machine_to_queue_on_name/:division_machine_to_queue_on_name',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/queue_player_after_play/confirm/confirm.html',
 	       controller: 'app.queue_player_after_play.confirm'
 	     }
 	   }
       }).state('app.queue_player_after_play.confirm.process', 
        { 
         cache: false,
 	 url: '/process',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/queue_player_after_play/confirm/process/process.html',
 	       controller: 'app.queue_player_after_play.confirm.process'
 	     }
 	   }, params: {
             process_step:{}
             
          }    

       })//REPLACE_ME



}]);
