angular.module('TDApp').config(['$stateProvider', '$urlRouterProvider',function($stateProvider, $urlRouterProvider) {    
    $stateProvider.state('app.token', 
        { 
         cache: false,
 	 url: '/token',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/token/token.html',
 	       controller: 'app.token'
 	     }
 	   }
       }).state('app.token.token_select', 
        { 
         cache: false,
 	 url: '/token_select/player_id/:player_id',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/token/token_select/token_select.html',
 	       controller: 'app.token.token_select'
 	     }
 	   }
       }).state('app.token.token_select.process', 
        { 
         cache: false,
 	 url: '/process',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/token/token_select/process/process.html',
 	       controller: 'app.token.token_select.process'
 	     }
 	   }, params: {
             process_step:{}
             ,token_info:{}             

          }    

       })//REPLACE_ME



}]);
