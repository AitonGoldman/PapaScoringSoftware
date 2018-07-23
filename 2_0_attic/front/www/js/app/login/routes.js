angular.module('TDApp').config(['$stateProvider', '$urlRouterProvider',function($stateProvider, $urlRouterProvider) {    
    $stateProvider.state('app.login', 
        { 
         cache: false,
 	 url: '/login',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/login/login.html',
 	       controller: 'app.login'
 	     }
 	   }
       }).state('app.login.process', 
        { 
         cache: false,
 	 url: '/process',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/login/process/process.html',
 	       controller: 'app.login.process'
 	     }
 	   }, params: {
             process_step:{}
             ,user_info:{}             

          }    

       })//REPLACE_ME


}]);
