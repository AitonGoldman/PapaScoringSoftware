angular.module('TDApp').config(['$stateProvider', '$urlRouterProvider',function($stateProvider, $urlRouterProvider) {    
    $stateProvider.state('prereg.step1.step2', 
        { 
         cache: false,
 	 url: '/step2',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/prereg/step1/step2/step2.html',
 	       controller: 'prereg.step1.step2'
 	     }
 	   }
       }).state('prereg.step1.step2.step3', 
        { 
         cache: false,
 	 url: '/step3',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/prereg/step1/step2/step3/step3.html',
 	       controller: 'prereg.step1.step2.step3'
 	     }
 	   }
       }).state('prereg.step1.step2.step3.step4', 
        { 
         cache: false,
 	 url: '/step4/linked_division_id/:linked_division_id',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/prereg/step1/step2/step3/step4/step4.html',
 	       controller: 'prereg.step1.step2.step3.step4'
 	     }
 	   }
       }).state('prereg.step1.step2.step3.step4.step5', 
        { 
         cache: false,
 	 url: '/step5/uploaded_file_name/:uploaded_file_name',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/prereg/step1/step2/step3/step4/step5/step5.html',
 	       controller: 'prereg.step1.step2.step3.step4.step5'
 	     }
 	   }
       }).state('prereg.step1.step2.step3.step4.step5.process', 
        { 
         cache: false,
 	 url: '/process/stripe_token/:stripe_token/player_id/:player_id',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/prereg/step1/step2/step3/step4/step5/process/process.html',
 	       controller: 'prereg.step1.step2.step3.step4.step5.process'
 	     }
 	   }, params: {
             process_step:{}
             
          }    

       })//REPLACE_ME





}]);
