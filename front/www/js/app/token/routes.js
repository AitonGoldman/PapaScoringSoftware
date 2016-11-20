angular.module('TDApp').config(['$stateProvider', '$urlRouterProvider',function($stateProvider, $urlRouterProvider) {    
    $stateProvider.state('app.token', 
        { 
         cache: false,
 	 url: '/token',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/token/token.html',
 	       controller: 'app.token'
 	     }
 	   }
       })//REPLACE_ME

}]);
