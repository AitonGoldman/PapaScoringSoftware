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
 	 url: '/queue/division_id/:division_id/start_range/:start_range/end_range/:end_range',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/queue_view/queue/queue.html',
 	       controller: 'app.queue_view.queue'
 	     }
 	   }
       })//REPLACE_ME


}]);
