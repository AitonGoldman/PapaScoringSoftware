angular.module('TDApp').config(['$stateProvider', '$urlRouterProvider',function($stateProvider, $urlRouterProvider) {    
    $stateProvider.state('app.queue_view', 
        { 
         cache: false,
 	 url: '/queue_view',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/queue_view/queue_view.html',
 	       controller: 'app.queue_view'
 	     }
 	   }
       }).state('app.queue_view.queue', 
        { 
         cache: false,
 	 url: '/queue/division_id/:division_id/game_1/:game_1/game_2/:game_2/game_3/:game_3/game_4/:game_4/game_5/:game_5/game_6/:game_6/game_7/:game_7/game_8/:game_8/game_9/:game_9/game_10/:game_10/game_11/:game_11/game_12/:game_12/columns/:columns',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/queue_view/queue/queue.html',
 	       controller: 'app.queue_view.queue'
 	     }
 	   }
       })//REPLACE_ME


}]);
