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
       })//REPLACE_ME


}]);
