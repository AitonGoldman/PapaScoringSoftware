angular.module('TDApp').config(['$stateProvider', '$urlRouterProvider',function($stateProvider, $urlRouterProvider) {    
    $stateProvider.state('app.i_need_an_adult', 
        { 
         cache: false,
 	 url: '/i_need_an_adult',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/i_need_an_adult/i_need_an_adult.html',
 	       controller: 'app.i_need_an_adult'
 	     }
 	   }
       }).state('app.i_need_an_adult.process', 
        { 
         cache: false,
 	 url: '/process/division_id/:division_id',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/i_need_an_adult/process/process.html',
 	       controller: 'app.i_need_an_adult.process'
 	     }
 	   }, params: {
             process_step:{}
             
          }    

       })//REPLACE_ME


}]);
