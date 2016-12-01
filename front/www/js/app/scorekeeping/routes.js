angular.module('TDApp').config(['$stateProvider', '$urlRouterProvider',function($stateProvider, $urlRouterProvider) {    
    $stateProvider.state('app.scorekeeping', 
        { 
         cache: false,
 	 url: '/scorekeeping',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/scorekeeping/scorekeeping.html',
 	       controller: 'app.scorekeeping'
 	     }
 	   }
       }).state('app.scorekeeping.machine_select', 
        { 
         cache: false,
 	 url: '/machine_select/division_id/:division_id',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/scorekeeping/machine_select/machine_select.html',
 	       controller: 'app.scorekeeping.machine_select'
 	     }
 	   }
       }).state('app.scorekeeping.machine_select.player_select', 
        { 
         cache: false,
 	 url: '/player_select/division_machine_id/:division_machine_id/division_machine_name/:division_machine_name/player_name/:player_name/player_id/:player_id',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/scorekeeping/machine_select/player_select/player_select.html',
 	       controller: 'app.scorekeeping.machine_select.player_select'
 	     }
 	   }
       }).state('app.scorekeeping.machine_select.player_select.process', 
        { 
         cache: false,
 	 url: '/process/player_id/:player_id/from_queue/:from_queue',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/scorekeeping/machine_select/player_select/process/process.html',
 	       controller: 'app.scorekeeping.machine_select.player_select.process'
 	     }
 	   }, params: {
               process_step:{},
               player_info:{}               
          }    

       }).state('app.scorekeeping.machine_select.record_score', 
        { 
         cache: false,
 	 url: '/record_score/division_machine_id/:division_machine_id/division_machine_name/:division_machine_name/player_name/:player_name/player_id/:player_id',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/scorekeeping/machine_select/record_score/record_score.html',
 	       controller: 'app.scorekeeping.machine_select.record_score'
 	     }
 	   }
       }).state('app.scorekeeping.machine_select.record_score.void', 
        { 
         cache: false,
 	 url: '/void',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/scorekeeping/machine_select/record_score/void/void.html',
 	       controller: 'app.scorekeeping.machine_select.record_score.void'
 	     }
 	 }, params: {
             process_step:{}
         }                                     
       }).state('app.scorekeeping.machine_select.record_score.confirm.process', 
        { 
         cache: false,
 	 url: '/process',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/scorekeeping/machine_select/record_score/confirm/process/process.html',
 	       controller: 'app.scorekeeping.machine_select.record_score.confirm.process'
 	     }
 	   }, params: {
             process_step:{}
             ,confirmed_score:{}             

          }    

       }).state('app.scorekeeping.machine_select.record_score.confirm', 
        { 
         cache: false,
 	 url: '/confirm/score/:score',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/scorekeeping/machine_select/record_score/confirm/confirm.html',
 	       controller: 'app.scorekeeping.machine_select.record_score.confirm'
 	     }
 	   }
       }).state('app.scorekeeping.machine_select.record_score.confirm.process.queue_add', 
        { 
         cache: false,
 	 url: '/queue_add',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/scorekeeping/machine_select/record_score/confirm/process/queue_add/queue_add.html',
 	       controller: 'app.scorekeeping.machine_select.record_score.confirm.process.queue_add'
 	     }
 	   }
       }).state('app.scorekeeping.machine_select.record_score.confirm.process.queue_add.process', 
        { 
         cache: false,
 	 url: '/process/division_machine_id/:queued_division_machine_id/:queued_division_machine_name',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/scorekeeping/machine_select/record_score/confirm/process/queue_add/process/process.html',
 	       controller: 'app.scorekeeping.machine_select.record_score.confirm.process.queue_add.process'
 	     }
 	   }, params: {
               process_step:{}               
             
          }    

       })//REPLACE_ME










}]);
