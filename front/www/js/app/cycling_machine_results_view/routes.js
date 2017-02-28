angular.module('TDApp').config(['$stateProvider', '$urlRouterProvider',function($stateProvider, $urlRouterProvider) {    
    $stateProvider.state('app.cycling_machine_results_view', 
        { 
         cache: false,
 	 url: '/cycling_machine_results_view/starting_division_machine_id/:starting_division_machine_id/division_id/:division_id',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/cycling_machine_results_view/cycling_machine_results_view.html',
 	       controller: 'app.cycling_machine_results_view'
 	     }
 	   }
       })//REPLACE_ME

}]);
