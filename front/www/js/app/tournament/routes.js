angular.module('TDApp').config(['$stateProvider', '$urlRouterProvider',function($stateProvider, $urlRouterProvider) {    
    $stateProvider.state('app.tournament', 
        { 
         cache: false,
 	 url: '/tournament',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/tournament/tournament.html',
 	       controller: 'app.tournament'
 	     }
 	   }
       }).state('app.tournament.add_tournament', 
        { 
         cache: false,
 	 url: '/add_tournament',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/tournament/add_tournament/add_tournament.html',
 	       controller: 'app.tournament.add_tournament'
 	     }
 	   }
       }).state('app.tournament.add_tournament.process', 
        { 
         cache: false,
 	 url: '/process',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/tournament/add_tournament/process/process.html',
 	       controller: 'app.tournament.add_tournament.process'
 	     }
 	   }, params: {
             process_step:{}
             ,tournament_info:{}             

          }    

       }).state('app.tournament.edit_tournament', 
        { 
         cache: false,
 	 url: '/edit_tournament/division_id/:division_id',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/tournament/edit_tournament/edit_tournament.html',
 	       controller: 'app.tournament.edit_tournament'
 	     }
 	   }
       }).state('app.tournament.edit_tournament.process', 
        { 
         cache: false,
 	 url: '/process',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/tournament/edit_tournament/process/process.html',
 	       controller: 'app.tournament.edit_tournament.process'
 	     }
 	   }, params: {
             process_step:{}
             ,division_info:{}             

          }    

       })//REPLACE_ME






}]);
