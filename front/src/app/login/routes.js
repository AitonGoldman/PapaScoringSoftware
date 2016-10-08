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
               template: 'poop'
             }
 	   }
       })//REPLACE_ME


}]);

