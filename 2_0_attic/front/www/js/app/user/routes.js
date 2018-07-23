angular.module('TDApp').config(['$stateProvider', '$urlRouterProvider',function($stateProvider, $urlRouterProvider) {    
    $stateProvider.state('app.user', 
        { 
         cache: false,
 	 url: '/user',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/user/user.html',
 	       controller: 'app.user'
 	     }
 	   }
       }).state('app.user.add_user', 
        { 
         cache: false,
 	 url: '/add_user',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/user/add_user/add_user.html',
 	       controller: 'app.user.add_user'
 	     },
             'edit_user@app.user.add_user':{
                 templateUrl: 'shared_html/edit_user.html'
             }
 	   }
       }).state('app.user.add_user.process', 
        { 
         cache: false,
 	 url: '/process',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/user/add_user/process/process.html',
 	       controller: 'app.user.add_user.process'
 	     }
 	   }, params: {
             process_step:{}
             ,user_info:{}             

          }    

       }).state('app.user.edit_user', 
        { 
         cache: false,
 	 url: '/edit_user/user_id/:user_id',
 	 views: {
 	     'menuContent@app': {
                 templateUrl: 'js/app/user/edit_user/edit_user.html',
 	         controller: 'app.user.edit_user'
 	     },
             'edit_user@app.user.edit_user':{
                 templateUrl: 'shared_html/edit_user.html'
             }
 	   }
       }).state('app.user.edit_user.process', 
        { 
         cache: false,
 	 url: '/process',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/user/edit_user/process/process.html',
 	       controller: 'app.user.edit_user.process'
 	     }
 	   }, params: {
             process_step:{}
             ,user_info:{}             

          }    

       })//REPLACE_ME





}]);
