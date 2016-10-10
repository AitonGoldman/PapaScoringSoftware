angular.module('TDApp').config(['$stateProvider', '$urlRouterProvider',function($stateProvider, $urlRouterProvider) {
    $urlRouterProvider.otherwise('/app');
    
    $stateProvider.state('app.login', 
        { 
 	 url: '/login',
 	 views: {
 	     '@': {
 	       templateUrl: 'app/login/login.html',
 	       controller: 'app.login'
 	     },
             'backbutton@':{
               templateUrl: 'shared_html/backbutton.html'
             },
             'title@':{
               template: 'Login'
             }
 	   }
       }).state('app.login.process', 
        { 
 	 url: '/process',
 	 views: {
 	     '@': {
 	       templateUrl: 'app/login/process/process.html',
 	       controller: 'app.login.process'
 	     },
             'backbutton@':{
               templateUrl: 'shared_html/backbutton.html'
             },
             'title@':{
               template: 'Logged In'
             }
 	   }, params: {
             process_step:{}
             ,user_info:{}             

          }
    

       })//REPLACE_ME



}]);

