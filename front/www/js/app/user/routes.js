angular.module('TDApp').config(['$stateProvider', '$urlRouterProvider',function($stateProvider, $urlRouterProvider) {    
    $stateProvider.state('app.user', 
        { 
         cache: false,
 	 url: '/user',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/user/user.html',
 	       controller: 'app.user'
 	     }
 	   }
       }).state('app.user.add_user', 
        { 
         cache: false,
 	 url: '/add_user',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/user/add_user/add_user.html',
 	       controller: 'app.user.add_user'
 	     }
 	   }
       }).state('app.user.add_user.process', 
        { 
         cache: false,
 	 url: '/process',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/user/add_user/process/process.html',
 	       controller: 'app.user.add_user.process'
 	     }
 	   }, params: {
             process_step:{}
             ,user_info:{}             

          }    

       })//REPLACE_ME



}]);
