angular.module('TDApp').config(['$stateProvider', '$urlRouterProvider',function($stateProvider, $urlRouterProvider) {    
    $stateProvider.state('app.login_player', 
        { 
         cache: false,
 	 url: '/login_player',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/login_player/login_player.html',
 	       controller: 'app.login_player'
 	     }
 	   }
       }).state('app.login_player.process', 
        { 
         cache: false,
 	 url: '/process',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/login_player/process/process.html',
 	       controller: 'app.login_player.process'
 	     }
 	   }, params: {
             process_step:{}
             ,player:{}             

          }    

       })//REPLACE_ME


}]);
