angular.module('TDApp').config(['$stateProvider', '$urlRouterProvider',function($stateProvider, $urlRouterProvider) {    
    $stateProvider.state('app.player', 
        { 
         cache: false,
 	 url: '/player',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/player/player.html',
 	       controller: 'app.player'
 	     }
 	   }
       }).state('app.player.add_player', 
        { 
         cache: false,
 	 url: '/add_player',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/player/add_player/add_player.html',
 	       controller: 'app.player.add_player'
 	     }
 	   }
       }).state('app.player.add_player.process', 
        { 
         cache: false,
 	 url: '/process',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/player/add_player/process/process.html',
 	       controller: 'app.player.add_player.process'
 	     }
 	   }, params: {
             process_step:{}
             ,player_info:{}             

          }    

       }).state('app.player.edit_player', 
        { 
         cache: false,
 	 url: '/edit_player/player_id/:player_id',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/player/edit_player/edit_player.html',
 	       controller: 'app.player.edit_player'
 	     }
 	   }
       }).state('app.player.edit_player.process', 
        { 
         cache: false,
 	 url: '/process',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/player/edit_player/process/process.html',
 	       controller: 'app.player.edit_player.process'
 	     }
 	   }, params: {
             process_step:{}
             ,player_info:{}             

          }    

       })//REPLACE_ME





}]);
