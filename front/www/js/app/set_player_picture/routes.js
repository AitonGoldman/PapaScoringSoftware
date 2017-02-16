angular.module('TDApp').config(['$stateProvider', '$urlRouterProvider',function($stateProvider, $urlRouterProvider) {    
    $stateProvider.state('app.set_player_picture', 
        { 
         cache: false,
 	 url: '/set_player_picture',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/set_player_picture/set_player_picture.html',
 	       controller: 'app.set_player_picture'
 	     }
 	   }
       }).state('app.set_player_picture.take_picture', 
        { 
         cache: false,
 	 url: '/take_picture/player_id/:player_id',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/set_player_picture/take_picture/take_picture.html',
 	       controller: 'app.set_player_picture.take_picture'
 	     }
 	   }
       }).state('app.set_player_picture.take_picture.process', 
        { 
         cache: false,
 	 url: '/process/pic_file/:pic_file',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/set_player_picture/take_picture/process/process.html',
 	       controller: 'app.set_player_picture.take_picture.process'
 	     }
 	   }, params: {
             process_step:{}
             
          }    

       })//REPLACE_ME



}]);
