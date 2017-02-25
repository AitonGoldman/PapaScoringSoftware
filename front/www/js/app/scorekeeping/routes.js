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
 	   }, params: {             
             hide_back_button:false             
          }
       }).state('app.scorekeeping.machine_select.player_select', 
        { 
         cache: false,
 	 url: '/player_select/division_machine_id/:division_machine_id/division_machine_name/:division_machine_name/player_name/:player_name/player_id/:player_id/previous_player_id/:previous_player_id/previous_player_name/:previous_player_name',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/scorekeeping/machine_select/player_select/player_select.html',
 	       controller: 'app.scorekeeping.machine_select.player_select'
 	     }
 	   }, params: {             
             hide_back_button:false             
          }
       }).state('app.scorekeeping.machine_select.player_select.process', 
        { 
         cache: false,
 	 url: '/process/player_id/:player_id/from_queue/:from_queue/existing_queue_machine/:existing_queue_machine',
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
 	 url: '/record_score/division_machine_id/:division_machine_id/division_machine_name/:division_machine_name/player_name/:player_name/player_id/:player_id/team/:team_tournament',
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

       }).state('app.scorekeeping.machine_select.team_select', 
        { 
         cache: false,
 	 url: '/team_select/division_machine_id/:division_machine_id/division_machine_name/:division_machine_name',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/scorekeeping/machine_select/team_select/team_select.html',
 	       controller: 'app.scorekeeping.machine_select.team_select'
 	     }
 	   }
       }).state('app.scorekeeping.machine_select.team_select.process', 
        { 
         cache: false,
 	 url: '/process/team_id/:team_id/team_name/:team_name',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/scorekeeping/machine_select/team_select/process/process.html',
 	       controller: 'app.scorekeeping.machine_select.team_select.process'
 	     }
 	   }, params: {
             process_step:{}
             ,team_info:{}             

          }    

       }).state('app.scorekeeping.machine_select.record_score.confirm_jagoff', 
        { 
         cache: false,
 	 url: '/confirm_jagoff',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/scorekeeping/machine_select/record_score/confirm_jagoff/confirm_jagoff.html',
 	       controller: 'app.scorekeeping.machine_select.record_score.confirm_jagoff'
 	     }
 	   }
       }).state('app.scorekeeping.machine_select.record_score.confirm_jagoff.process', 
        { 
         cache: false,
 	 url: '/process',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/scorekeeping/machine_select/record_score/confirm_jagoff/process/process.html',
 	       controller: 'app.scorekeeping.machine_select.record_score.confirm_jagoff.process'
 	     }
 	   }, params: {
             process_step:{}
             
          }    

       }).state('app.scorekeeping.undo', 
        { 
         cache: false,
 	 url: '/undo/division_id/:division_id',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/scorekeeping/undo/undo.html',
 	       controller: 'app.scorekeeping.undo'
 	     }
 	   }
       }).state('app.scorekeeping.undo.remove_player', 
        { 
         cache: false,
 	 url: '/remove_player',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/scorekeeping/undo/remove_player/remove_player.html',
 	       controller: 'app.scorekeeping.undo.remove_player'
 	     }
 	   }
       }).state('app.scorekeeping.undo.remove_player.confirm', 
        { 
         cache: false,
 	 url: '/confirm/division_machine_id/:division_machine_id/division_machine_name/:division_machine_name/player_id/:player_id/player_name/:player_name',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/scorekeeping/undo/remove_player/confirm/confirm.html',
 	       controller: 'app.scorekeeping.undo.remove_player.confirm'
 	     }
 	   }
       }).state('app.scorekeeping.undo.remove_player.confirm.process', 
        { 
         cache: false,
 	 url: '/process',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/scorekeeping/undo/remove_player/confirm/process/process.html',
 	       controller: 'app.scorekeeping.undo.remove_player.confirm.process'
 	     }
 	   }, params: {
             process_step:{}
             
          }    

       }).state('app.scorekeeping.undo.remove_player.confirm.process.add_player', 
        { 
         cache: false,
 	 url: '/add_player',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/scorekeeping/undo/remove_player/confirm/process/add_player/add_player.html',
 	       controller: 'app.scorekeeping.undo.remove_player.confirm.process.add_player'
 	     }
 	   }
       }).state('app.scorekeeping.undo.remove_player.confirm.process.add_player.confirm', 
        { 
         cache: false,
 	 url: '/confirm/player_id_to_add/:player_id_to_add/player_name_to_add/:player_name_to_add',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/scorekeeping/undo/remove_player/confirm/process/add_player/confirm/confirm.html',
 	       controller: 'app.scorekeeping.undo.remove_player.confirm.process.add_player.confirm'
 	     }
 	   }
       }).state('app.scorekeeping.undo.remove_player.confirm.process.add_player.confirm.process', 
        { 
         cache: false,
 	 url: '/process',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/scorekeeping/undo/remove_player/confirm/process/add_player/confirm/process/process.html',
 	       controller: 'app.scorekeeping.undo.remove_player.confirm.process.add_player.confirm.process'
 	     }
 	   }, params: {
             process_step:{}
             
          }    

       }).state('app.scorekeeping.undo.remove_player.confirm.process.add_player.process', 
        { 
         cache: false,
 	 url: '/process/player_id_to_add/:player_id_to_add/player_name_to_add/:player_name_to_add',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/scorekeeping/undo/remove_player/confirm/process/add_player/process/process.html',
 	       controller: 'app.scorekeeping.undo.remove_player.confirm.process.add_player.process'
 	     }
 	   }, params: {
             process_step:{}
             
          }    

       }).state('app.scorekeeping.machine_select.select_action', 
        { 
         cache: false,
 	 url: '/select_action/division_machine_id/:division_machine_id',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/scorekeeping/machine_select/select_action/select_action.html',
 	       controller: 'app.scorekeeping.machine_select.select_action'
 	     }
 	   }
       }).state('app.scorekeeping.machine_select.add_player_to_queue', 
        { 
         cache: false,
 	 url: '/add_player_to_queue/division_machine_id/:division_machine_id/division_machine_name/:division_machine_name',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/scorekeeping/machine_select/add_player_to_queue/add_player_to_queue.html',
 	       controller: 'app.scorekeeping.machine_select.add_player_to_queue'
 	     }
 	   }
       }).state('app.scorekeeping.machine_select.add_player_to_queue.confirm', 
        { 
         cache: false,
 	 url: '/confirm/player_id/:player_id/player_name/:player_name',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/scorekeeping/machine_select/add_player_to_queue/confirm/confirm.html',
 	       controller: 'app.scorekeeping.machine_select.add_player_to_queue.confirm'
 	     }
 	   }
       }).state('app.scorekeeping.machine_select.add_player_to_queue.confirm.process', 
        { 
         cache: false,
 	 url: '/process',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/scorekeeping/machine_select/add_player_to_queue/confirm/process/process.html',
 	       controller: 'app.scorekeeping.machine_select.add_player_to_queue.confirm.process'
 	     }
 	   }, params: {
             process_step:{}
             
          }    

       })//REPLACE_ME


























}]);
