angular.module('TDApp').config(['$stateProvider', '$urlRouterProvider',function($stateProvider, $urlRouterProvider) {    
    $stateProvider.state('app.finals', 
        { 
         cache: false,
 	 url: '/finals',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/finals/finals.html',
 	       controller: 'app.finals'
 	     }
 	   }
       }).state('app.finals.manage', 
        { 
         cache: false,
 	 url: '/manage/division_id/:division_id',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/finals/manage/manage.html',
 	       controller: 'app.finals.manage'
 	     }
 	   }
       }).state('app.finals.manage.tiebreakers', 
        { 
         cache: false,
 	 url: '/tiebreakers/division_final_id/:division_final_id',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/finals/manage/tiebreakers/tiebreakers.html',
 	       controller: 'app.finals.manage.tiebreakers'
 	     }
 	   }
       }).state('app.finals.manage.tiebreakers.resolve', 
        { 
         cache: false,
 	 url: '/resolve/rank_to_resolve/:rank_to_resolve',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/finals/manage/tiebreakers/resolve/resolve.html',
 	       controller: 'app.finals.manage.tiebreakers.resolve'
 	     }
 	   }
       }).state('app.finals.manage.rollcall', 
        { 
         cache: false,
 	 url: '/rollcall/division_final_id/:division_final_id',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/finals/manage/rollcall/rollcall.html',
 	       controller: 'app.finals.manage.rollcall'
 	     }
 	   }
       })//REPLACE_ME





}]);
