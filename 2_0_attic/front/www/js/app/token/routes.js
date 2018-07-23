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
 	   }, params: {             
             hide_back_button:false             
          }
       }).state('app.token_comp', 
        { 
         cache: false,
 	 url: '/token_comp',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/token/token.html',
 	       controller: 'app.token'
 	     }
 	   }, params: {             
             hide_back_button:false             
          }
       }).state('app.token.token_select', 
        { 
         cache: false,
 	 url: '/token_select/player_id/:player_id',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/token/token_select/token_select.html',
 	       controller: 'app.token.token_select'
 	     }
 	   }, params: {             
             hide_back_button:false             
          }
       }).state('app.token_comp.token_select_comp', 
        { 
         cache: false,
 	 url: '/token_select_comp/player_id/:player_id',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/token/token_select/token_select.html',
 	       controller: 'app.token.token_select'
 	     }
 	   }, params: {             
             hide_back_button:false             
          }
       }).state('app.token_comp.token_select_comp.confirm', 
        { 
         cache: false,
 	 url: '/confirm',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/token/token_select/confirm/confirm.html',
 	       controller: 'app.token.token_select.confirm'
 	     }
 	 }, params: {             
             token_info:{}             
          } 
            
       }).state('app.token_comp.token_select_comp.confirm.process', 
        { 
         cache: false,
 	 url: '/process',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/token/token_select/confirm/process/process.html',
 	       controller: 'app.token.token_select.confirm.process'
 	     }
 	   }, params: {
               process_step:{}
               ,token_info:{},
               total_cost:undefined
          }    

       }).state('app.token.token_select.process', 
        { 
         cache: false,
 	 url: '/process',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/token/token_select/process/process.html',
 	       controller: 'app.token.token_select.process'
 	     }
 	   }, params: {
             process_step:{}
             ,token_info:{}             

          }    

       }).state('app.token.token_select.confirm', 
        { 
         cache: false,
 	 url: '/confirm',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/token/token_select/confirm/confirm.html',
 	       controller: 'app.token.token_select.confirm'
 	     }
 	 }, params: {             
             token_info:{}             
          } 
            
       }).state('app.token.token_select.confirm.process', 
        { 
         cache: false,
 	 url: '/process',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/token/token_select/confirm/process/process.html',
 	       controller: 'app.token.token_select.confirm.process'
 	     }
 	   }, params: {
               process_step:{}
               ,token_info:{},
               total_cost:undefined
          }    

       })//REPLACE_ME



}]);
