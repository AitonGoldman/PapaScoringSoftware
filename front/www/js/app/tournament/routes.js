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

       }).state('app.tournament.division_list', 
        { 
         cache: false,
 	 url: '/division_list/tournament_id/:tournament_id',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/tournament/division_list/division_list.html',
 	       controller: 'app.tournament.division_list'
 	     }
 	   }
       }).state('app.tournament.division_list.add_division', 
        { 
         cache: false,
 	 url: '/add_division/tournament_id/:tournament_id',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/tournament/division_list/add_division/add_division.html',
 	       controller: 'app.tournament.division_list.add_division'
 	     }
 	   }
       }).state('app.tournament.division_list.add_division.process', 
        { 
         cache: false,
 	 url: '/process',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/tournament/division_list/add_division/process/process.html',
 	       controller: 'app.tournament.division_list.add_division.process'
 	     }
 	   }, params: {
             process_step:{}
             ,division_info:{}             

          }    

       }).state('app.tournament.division_list.edit_division', 
        { 
         cache: false,
 	 url: '/edit_division/division_id/:division_id',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/tournament/division_list/edit_division/edit_division.html',
 	       controller: 'app.tournament.division_list.edit_division'
 	     }
 	   }
       }).state('app.tournament.division_list.edit_division.process', 
        { 
         cache: false,
 	 url: '/process',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/tournament/division_list/edit_division/process/process.html',
 	       controller: 'app.tournament.division_list.edit_division.process'
 	     }
 	   }, params: {
             process_step:{}
             ,division_info:{}             

          }    

       })//REPLACE_ME











}]);
