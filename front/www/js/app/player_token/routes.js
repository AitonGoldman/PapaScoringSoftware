angular.module('TDApp').config(['$stateProvider', '$urlRouterProvider',function($stateProvider, $urlRouterProvider) {    
    $stateProvider.state('app.player_token', 
        { 
         cache: false,
 	 url: '/player_token',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/player_token/player_token.html',
 	       controller: 'app.player_token'
 	     }
 	   }
       }).state('app.player_token.confirm', 
        { 
         cache: false,
 	 url: '/confirm',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/player_token/confirm/confirm.html',
 	       controller: 'app.player_token.confirm'
 	     }
 	 }, params: {             
             token_info:{}             
          } 
            
       }).state('app.player_token.confirm.process', 
        { 
         cache: false,
 	 url: '/process',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/player_token/confirm/process/process.html',
 	       controller: 'app.player_token.confirm.process'
 	     }
 	   }, params: {
             process_step:{}
             ,token_info:{}             

          }    

       })//REPLACE_ME




}]);
