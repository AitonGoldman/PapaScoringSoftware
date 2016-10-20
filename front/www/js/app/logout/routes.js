angular.module('TDApp').config(['$stateProvider', '$urlRouterProvider',function($stateProvider, $urlRouterProvider) {    
    $stateProvider.state('app.logout', 
        { 
         cache: false,
 	 url: '/logout',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/logout/logout.html',
 	       controller: 'app.logout'
 	     }
 	   }
       })//REPLACE_ME

}]);
