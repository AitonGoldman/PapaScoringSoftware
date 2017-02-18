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
 	 url: '/division_final/division_final_id/:division_final_id',
 	 views: {
 	     'menuContent@app': {
 	       templateUrl: 'js/app/finals_scorekeeper/division_final/division_final.html',
 	       controller: 'app.finals_scorekeeper.division_final'
 	     }
 	   }
       }).state('app.finals_scorekeeper.division_final.round_0', {
           url: "/round/:round_idx",
           views: {
               'round_tab@app.finals_scorekeeper.division_final': {
                   templateUrl: "js/app/finals_scorekeeper/division_final/test.html",
                   controller: 'app.finals_scorekeeper.division_final.round'
               }                             
           },
           data: {
               round: 0               
           }  
       }).state('app.finals_scorekeeper.division_final.round_1', {
           url: "/round/:round_idx",
           views: {
               'round_tab@app.finals_scorekeeper.division_final': {
                   templateUrl: "js/app/finals_scorekeeper/division_final/test.html",
                   controller: 'app.finals_scorekeeper.division_final.round'
               }                             
           },
           data: {
               round: 0               
           }  
       }).state('app.finals_scorekeeper.division_final.round_2', {
           url: "/round/:round_idx",
           views: {
               'round_tab@app.finals_scorekeeper.division_final': {
                   templateUrl: "js/app/finals_scorekeeper/division_final/test.html",
                   controller: 'app.finals_scorekeeper.division_final.round'
               }                             
           },
           data: {
               round: 0               
           }  
       }).state('app.finals_scorekeeper.division_final.round_3', {
           url: "/round/:round_idx",
           views: {
               'round_tab@app.finals_scorekeeper.division_final': {
                   templateUrl: "js/app/finals_scorekeeper/division_final/test.html",
                   controller: 'app.finals_scorekeeper.division_final.round'
               }                             
           },
           data: {
               round: 0               
           }  
       }).state('app.finals_scorekeeper.division_final.round_0.match_details', {
            url: "/match_details/:division_final_match_id/:division_final_match_idx/:round_idx",
            views: {
                'round_tab@app.finals_scorekeeper.division_final': {
                    templateUrl: "js/app/finals_scorekeeper/division_final/division_final_match.html",
                    controller: 'app.finals_scorekeeper.division_final.round.match_details'                    
                }               

            }
       }).state('app.finals_scorekeeper.division_final.round_1.match_details', {
            url: "/match_details/:division_final_match_id/:division_final_match_idx/:round_idx",
            views: {
                'round_tab@app.finals_scorekeeper.division_final': {
                    templateUrl: "js/app/finals_scorekeeper/division_final/division_final_match.html",
                    controller: 'app.finals_scorekeeper.division_final.round.match_details'                    
                }               

            }
       }).state('app.finals_scorekeeper.division_final.round_2.match_details', {
            url: "/match_details/:division_final_match_id/:division_final_match_idx/:round_idx",
            views: {
                'round_tab@app.finals_scorekeeper.division_final': {
                    templateUrl: "js/app/finals_scorekeeper/division_final/division_final_match.html",
                    controller: 'app.finals_scorekeeper.division_final.round.match_details'                    
                }               

            }
       }).state('app.finals_scorekeeper.division_final.round_3.match_details', {
            url: "/match_details/:division_final_match_id/:division_final_match_idx/:round_idx",
            views: {
                'round_tab@app.finals_scorekeeper.division_final': {
                    templateUrl: "js/app/finals_scorekeeper/division_final/division_final_match.html",
                    controller: 'app.finals_scorekeeper.division_final.round.match_details'                    
                }               

            }
       })//REPLACE_ME
    


}]);
