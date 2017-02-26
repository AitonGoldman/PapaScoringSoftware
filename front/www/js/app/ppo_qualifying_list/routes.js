angular.module('TDApp').config(['$stateProvider', '$urlRouterProvider',function($stateProvider, $urlRouterProvider) {    
    $stateProvider.state('app.ppo_qualifying_list', 
        { 
         cache: false,
 	 url: '/ppo_qualifying_list',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/ppo_qualifying_list/ppo_qualifying_list.html',
 	       controller: 'app.ppo_qualifying_list'
 	     }
 	   }
       }).state('app.ppo_qualifying_list.qualifiers', 
        { 
         cache: false,
 	 url: '/qualifiers/division_id/:division_id',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/ppo_qualifying_list/qualifiers/qualifiers.html',
 	       controller: 'app.ppo_qualifying_list.qualifiers'
 	     }
 	   }
       }).state('app.ppo_qualifying_list.papa_qualifiers', 
        { 
         cache: false,
 	 url: '/papa_qualifiers/division_id/:division_id',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/ppo_qualifying_list/papa_qualifiers/papa_qualifiers.html',
 	       controller: 'app.ppo_qualifying_list.papa_qualifiers'
 	     }
 	   }
       })//REPLACE_ME



}]);
