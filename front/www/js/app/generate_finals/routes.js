angular.module('TDApp').config(['$stateProvider', '$urlRouterProvider',function($stateProvider, $urlRouterProvider) {    
    $stateProvider.state('app.generate_finals', 
        { 
         cache: false,
 	 url: '/generate_finals/:division_id',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/generate_finals/generate_finals.html',
 	       controller: 'app.generate_finals'
 	     }
 	   }, params: {
                 process_step:{},
                 papa_qualifiers:{},
                 ppo_a_qualifiers:{},
                 ppo_b_qualifiers:{}
             }
       })//REPLACE_ME

}]);
