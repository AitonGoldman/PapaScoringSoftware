angular.module('TDApp').config(['$stateProvider', '$urlRouterProvider',function($stateProvider, $urlRouterProvider) {    
    $stateProvider.state('app.finals_scorekeeper', 
        { 
         cache: false,
 	 url: '/finals_scorekeeper',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/finals_scorekeeper/finals_scorekeeper.html',
 	       controller: 'app.finals_scorekeeper'
 	     }
 	   }
       }).state('app.finals_scorekeeper.division_final', 
        { 
         cache: false,
 	 url: '/division_final/division_final_id/:division_final_id/round/:round_id',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/finals_scorekeeper/division_final/division_final.html',
 	       controller: 'app.finals_scorekeeper.division_final'
 	     }
 	   }
        }).state('app.finals_scorekeeper.division_final.match', 
        { 
         cache: false,
 	 url: '/match/match_id/:match_id',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/finals_scorekeeper/division_final/match/match.html',
 	       controller: 'app.finals_scorekeeper.division_final.match'
 	     }
 	   }
       }).state('app.finals_scorekeeper.division_final.match.play_order', 
        { 
         cache: false,
 	 url: '/play_order/:game_index',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/finals_scorekeeper/division_final/match/play_order/play_order.html',
 	       controller: 'app.finals_scorekeeper.division_final.match.play_order'
 	     }
 	   }
       }).state('app.finals_scorekeeper.division_final.match.resolve_tiebreaker', 
        { 
         cache: false,
 	 url: '/resolve_tiebreaker',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/finals_scorekeeper/division_final/match/resolve_tiebreaker/resolve_tiebreaker.html',
 	       controller: 'app.finals_scorekeeper.division_final.match.resolve_tiebreaker'
 	     }
 	   }
       }).state('app.finals_results', 
        { 
         cache: false,
 	 url: '/finals_results',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/finals_scorekeeper/finals_scorekeeper.html',
 	       controller: 'app.finals_scorekeeper'
 	     }
 	   }
       }).state('app.finals_results.division_final', 
        { 
         cache: false,
 	 url: '/division_final/division_final_id/:division_final_id/round/:round_id',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/finals_scorekeeper/division_final/division_final.html',
 	       controller: 'app.finals_scorekeeper.division_final'
 	     }
 	   }
        }).state('app.finals_results.division_final.match', 
        { 
         cache: false,
 	 url: '/match/match_id/:match_id',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/finals_scorekeeper/division_final/match/match.html',
 	       controller: 'app.finals_scorekeeper.division_final.match'
 	     }
 	   }
       })//REPLACE_ME



}]);
