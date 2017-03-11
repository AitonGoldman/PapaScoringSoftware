angular.module('TDApp').config(['$stateProvider', '$urlRouterProvider',function($stateProvider, $urlRouterProvider) {    
    $stateProvider.state('app.prereg_complete', 
        { 
         cache: false,
 	 url: '/prereg_complete',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/prereg_complete/prereg_complete.html',
 	       controller: 'app.prereg_complete'
 	     }
 	   }
       }).state('app.prereg_complete.confirm', 
        { 
         cache: false,
 	 url: '/confirm/player_id/:player_id/player_name/:player_name',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/prereg_complete/confirm/confirm.html',
 	       controller: 'app.prereg_complete.confirm'
 	     }
 	   }
       }).state('app.prereg_complete.confirm.process', 
        { 
         cache: false,
 	 url: '/process',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/prereg_complete/confirm/process/process.html',
 	       controller: 'app.prereg_complete.confirm.process'
 	     }
 	   }, params: {
             process_step:{}
             
          }    

       }).state('app.in_line_complete', 
        { 
         cache: false,
 	 url: '/in_line_complete',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/prereg_complete/prereg_complete.html',
 	       controller: 'app.prereg_complete'
 	     }
 	   }
       }).state('app.in_line_complete.confirm', 
        { 
         cache: false,
 	 url: '/confirm/player_id/:player_id/player_name/:player_name',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/prereg_complete/confirm/confirm.html',
 	       controller: 'app.prereg_complete.confirm'
 	     }
 	   }
       }).state('app.in_line_complete.confirm.process', 
        { 
         cache: false,
 	 url: '/process',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/prereg_complete/confirm/process/process.html',
 	       controller: 'app.prereg_complete.confirm.process'
 	     }
 	   }, params: {
             process_step:{}
             
          }    

       })//REPLACE_ME



}]);
