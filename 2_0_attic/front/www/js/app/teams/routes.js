angular.module('TDApp').config(['$stateProvider', '$urlRouterProvider',function($stateProvider, $urlRouterProvider) {    
    $stateProvider.state('app.teams', 
        { 
         cache: false,
 	 url: '/teams',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/teams/teams.html',
 	       controller: 'app.teams'
 	     }
 	   }
       }).state('app.teams.add_team', 
        { 
         cache: false,
 	 url: '/add_team',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/teams/add_team/add_team.html',
 	       controller: 'app.teams.add_team'
 	     }
 	   }
       }).state('app.teams.add_team.process', 
        { 
         cache: false,
 	 url: '/process',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/teams/add_team/process/process.html',
 	       controller: 'app.teams.add_team.process'
 	     }
 	   }, params: {
             process_step:{}
             ,team_info:{}             

          }    

       })//REPLACE_ME



}]);
