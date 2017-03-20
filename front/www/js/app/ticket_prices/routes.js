angular.module('TDApp').config(['$stateProvider', '$urlRouterProvider',function($stateProvider, $urlRouterProvider) {    
    $stateProvider.state('app.ticket_prices', 
        { 
         cache: false,
 	 url: '/ticket_prices',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/ticket_prices/ticket_prices.html',
 	       controller: 'app.ticket_prices'
 	     }
 	   }
       })//REPLACE_ME

}]);
