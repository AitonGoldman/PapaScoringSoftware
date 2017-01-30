angular.module('TDApp').config(['$stateProvider', '$urlRouterProvider',function($stateProvider, $urlRouterProvider) {    
    $stateProvider.state('app.queues', 
        { 
         cache: false,
 	 url: '/queues/manage/:manage',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/queues/queues.html',
 	       controller: 'app.queues'
 	     }
 	   }
       }).state('app.queues.machine_select', 
        { 
         cache: false,
 	 url: '/machine_select/division_id/:division_id',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/queues/machine_select/machine_select.html',
 	       controller: 'app.queues.machine_select'
 	     }
 	   }
       }).state('app.queues.machine_select.machine_queue', 
        { 
         cache: false,
 	 url: '/machine_queue/division_machine_id/:division_machine_id/division_machine_name/:division_machine_name',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/queues/machine_select/machine_queue/machine_queue.html',
 	       controller: 'app.queues.machine_select.machine_queue'
 	     }
 	   }
       }).state('app.queues.machine_select.machine_queue.player_select', 
        { 
         cache: false,
 	 url: '/player_select',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/queues/machine_select/machine_queue/player_select/player_select.html',
 	       controller: 'app.queues.machine_select.machine_queue.player_select'
 	     }
 	   }
       }).state('app.queues.machine_select.machine_queue.player_select.confirm', 
        { 
         cache: false,
 	 url: '/confirm/player_id/:player_id/player_name/:player_name',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/queues/machine_select/machine_queue/player_select/confirm/confirm.html',
 	       controller: 'app.queues.machine_select.machine_queue.player_select.confirm'
 	     }
 	   }
       }).state('app.queues.machine_select.machine_queue.confirm', 
        { 
         cache: false,
 	 url: '/confirm/player_id/:player_id/player_name/:player_name',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/queues/machine_select/machine_queue/player_select/confirm/confirm.html',
 	       controller: 'app.queues.machine_select.machine_queue.player_select.confirm'
 	     }
 	   }
       }).state('app.queues.machine_select.machine_queue.player_select.confirm.process', 
        { 
         cache: false,
 	 url: '/process',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/queues/machine_select/machine_queue/player_select/confirm/process/process.html',
 	       controller: 'app.queues.machine_select.machine_queue.player_select.confirm.process'
 	     }
 	   }, params: {
             process_step:{}
             
          }    

       }).state('app.queues.machine_select.machine_queue.confirm.process', 
        { 
         cache: false,
 	 url: '/process',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/queues/machine_select/machine_queue/player_select/confirm/process/process.html',
 	       controller: 'app.queues.machine_select.machine_queue.player_select.confirm.process'
 	     }
 	   }, params: {
             process_step:{}
             
          }    

       }).state('app.queues.machine_select.machine_queue.add_other_player', 
        { 
         cache: false,
 	 url: '/add_other_player',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/queues/machine_select/machine_queue/add_other_player/add_other_player.html',
 	       controller: 'app.queues.machine_select.machine_queue.add_other_player'
 	     }
 	   }
       }).state('app.queues.machine_select.machine_queue.add_other_player.process', 
        { 
         cache: false,
 	 url: '/process/other_player_id/:other_player_id/other_player_pin/:other_player_pin',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/queues/machine_select/machine_queue/add_other_player/process/process.html',
 	       controller: 'app.queues.machine_select.machine_queue.add_other_player.process'
 	     }
 	   }, params: {
             process_step:{}
             
          }    

       })//REPLACE_ME











}]);
