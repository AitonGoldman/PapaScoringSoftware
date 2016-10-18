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
       })//REPLACE_ME

}]);
