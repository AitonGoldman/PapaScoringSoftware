angular.module('TDApp').config(['$stateProvider', '$urlRouterProvider',function($stateProvider, $urlRouterProvider) {    
    $stateProvider.state('app.jagoffs', 
        { 
         cache: false,
 	 url: '/jagoffs',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/jagoffs/jagoffs.html',
 	       controller: 'app.jagoffs'
 	     }
 	   }
       })//REPLACE_ME

}]);
