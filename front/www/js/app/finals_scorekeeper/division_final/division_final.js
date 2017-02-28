angular.module('app.finals_scorekeeper.division_final',['app.finals_scorekeeper.division_final.round',
                                                        /*REPLACEMECHILD*/]);
angular.module('app.finals_scorekeeper.division_final').controller(
    'app.finals_scorekeeper.division_final',[
        '$scope','$state','TimeoutResources','Utils','Modals','$ionicHistory',
        function($scope, $state, TimeoutResources, Utils,Modals,$ionicHistory) {
            $scope.site=$state.params.site;
	    $scope.division_final_id=$state.params.division_final_id;
        $scope.utils = Utils;
        Modals.loading();
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                                
        finals_promise = TimeoutResources.GetDivisionFinals($scope.bootstrap_promise,{site:$scope.site});        
        // = TimeoutResources.GetEtcData();
        finals_promise.then(function(data){
            $scope.resources = TimeoutResources.GetAllResources();
            Modals.loaded();            
            $scope.rounds_length = $scope.resources.finals.data[$scope.division_final_id].division_final_rounds.length;            
            console.log($scope.rounds_length);
        });
            
        //Modals.loading();
        // = TimeoutResources.GetEtcData();
        //.then(function(data){
        // $scope.resources = TimeoutResources.GetAllResources();
        //  Modals.loaded();
        //})
    }]
);


angular.module('app.finals_scorekeeper.division_final.round',['app.finals_scorekeeper.division_final.round.match_details',
                                                              'app.finals_scorekeeper.division_final.round.tiebreaker',
                                                              /*REPLACEMECHILD*/]);
angular.module('app.finals_scorekeeper.division_final.round').controller(
    'app.finals_scorekeeper.division_final.round',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        //$scope.site=$state.params.site;
	$scope.division_final_id=$state.params.division_final_id;
        //$scope.utils = Utils;
        $scope.counter = $state.params.counter;
        $scope.round_idx = $state.params.round_idx;
        finals_promise = TimeoutResources.GetDivisionFinals(undefined,{site:$scope.site});                
        finals_promise.then(function(data){
            $scope.resources = TimeoutResources.GetAllResources();            
            Modals.loaded();                                        
        });                                                
        $scope.check_round_ready_to_be_completed = function(round_idx){
            if($scope.resources == undefined || $scope.resources.finals.data == undefined){
                return false;
            }
            round = $scope.resources.finals.data[$scope.division_final_id].division_final_rounds[round_idx];
            matches = round.division_final_matches;
            completed_matches_count =  _.filter(matches, function(o) { return o.completed == true; }).length;                                    
            if(completed_matches_count ==  $scope.resources.finals.data[$scope.division_final_id].division_final_rounds[round_idx].division_final_matches.length && round.completed == false){
                return true;
            }
            return false;
        };
        $scope.check_match_has_tiebreaker = function(division_machine_match){            
            if($scope.resources == undefined){
                return false;
            }

            if(division_machine_match.has_tiebreaker && division_machine_match.completed == false){
                return true;
            } else {
                return false;
            }
        };                
        $scope.check_match_ready_to_be_completed = function(division_machine_match){            
            completed_games_count =  _.filter(division_machine_match.finals_match_game_results, function(o) { return o.completed == true; }).length;            
            if(completed_games_count == 3 && division_machine_match.completed == false && division_machine_match.has_tiebreaker == false){
                return true;
            }
            return false;
        };
        $scope.setDivisionFinalRoundComplete = function(division_final_round){
            Modals.loading();
            division_final_round.completed=true;
            complete_promise = TimeoutResources.SetDivisionFinalRoundComplete(undefined,{site:$scope.site,division_final_round_id:division_final_round.division_final_round_id});
            complete_promise.then(function(data){
                finals_promise = TimeoutResources.GetDivisionFinals(undefined,{site:$scope.site});                
                finals_promise.then(function(data){
                    $scope.resources = TimeoutResources.GetAllResources();
                    Modals.loaded();
                    if (division_final_round.round_number != $scope.resources.finals.data[$scope.division_final_id].division_final_rounds.length){
                        Modals.information("Round Completed!  Next round is ready to start!");
                    } else {
                        Modals.information("Finals Completed!  We're all gonna get laid!");
                    }
                });                                                
            });
        };
        
        $scope.setDivisionFinalMatchComplete = function(division_final_match){
            Modals.loading();
            division_final_match.completed=true;
            complete_promise = TimeoutResources.SetDivisionFinalMatchComplete(undefined,{site:$scope.site,division_final_match_id:division_final_match.division_final_match_id});
            complete_promise.then(function(data){
                finals_promise = TimeoutResources.GetDivisionFinals(undefined,{site:$scope.site});                
                finals_promise.then(function(data){
                    $scope.resources = TimeoutResources.GetAllResources();
                    Modals.loaded();                                        
                });                                                
            });
        };
        
        //$scope.division_final_match_id = $state.params.division_final_match_id;
        //alert($scope.division_final_match_id);
        //Modals.loading();
        // = TimeoutResources.GetEtcData();
        //.then(function(data){
        // $scope.resources = TimeoutResources.GetAllResources();
        //  Modals.loaded();
        //})
    }]
);


angular.module('app.finals_scorekeeper.division_final.round.tiebreaker',[/*REPLACEMECHILD*/]);
angular.module('app.finals_scorekeeper.division_final.round.tiebreaker').controller(
    'app.finals_scorekeeper.division_final.round.tiebreaker',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;
        $scope.counter = $state.params.counter;
        $scope.division_final_match_id = $state.params.division_final_match_id;
        $scope.division_final_match_idx = $state.params.division_final_match_idx;
        $scope.round_idx = $state.params.round_idx;
        $scope.division_final_id = $state.params.division_final_id;        
        Modals.loading();
        finals_promise = TimeoutResources.GetDivisionFinals($scope.bootstrap_promise,{site:$scope.site});        
        // = TimeoutResources.GetEtcData();
        finals_promise.then(function(data){
            $scope.resources = TimeoutResources.GetAllResources();
            Modals.loaded();
            matches = $scope.resources.finals.data[$scope.division_final_id].division_final_rounds[$scope.round_idx].division_final_matches;
            $scope.match =  _.filter(matches, function(o) { return o.division_final_match_id == $scope.division_final_match_id; })[0];
            $scope.tiebreaker_players = _.filter($scope.match.finals_match_player_results,function(o){return o.needs_tiebreaker == true;});
            _.forEach($scope.tiebreaker_players, function(value, key) {
                $scope.tiebreaker_players[key].won_tiebreaker=false;
            });       
        });
        
        $scope.set_tiebreaker_winners = function(){
            finalsmatchplayerresult_ids=[];
            _.forEach($scope.tiebreaker_players, function(value, key) {
                
                finalsmatchplayerresult_ids.push([value.finals_player_id,value.won_tiebreaker]);
            });            
            Modals.loading();
            set_tiebreaker_promise = TimeoutResources.SetFinalsMatchTiebreakerWinners(undefined,{site:$scope.site},{division_final_match_id:$scope.match.division_final_match_id,data:finalsmatchplayerresult_ids});
            set_tiebreaker_promise.then(function(data){
                $state.go('.^');
                Modals.loaded();
            });
        };
    }]);


angular.module('app.finals_scorekeeper.division_final.round.match_details',[/*REPLACEMECHILD*/]);
angular.module('app.finals_scorekeeper.division_final.round.match_details').controller(
    'app.finals_scorekeeper.division_final.round.match_details',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        //$scope.site=$state.params.site;
	//$scope.division_final_id=$state.params.division_final_id;

        //$scope.utils = Utils;
        $scope.counter = $state.params.counter;
        $scope.division_final_match_id = $state.params.division_final_match_id;
        $scope.division_final_match_idx = $state.params.division_final_match_idx;
        $scope.round_idx = $state.params.round_idx;
        $scope.division_final_id = $state.params.division_final_id;        
        finals_promise = TimeoutResources.GetDivisionFinals($scope.bootstrap_promise,{site:$scope.site});        
        // = TimeoutResources.GetEtcData();
        finals_promise.then(function(data){
            $scope.resources = TimeoutResources.GetAllResources();
            Modals.loaded();
            matches = $scope.resources.finals.data[$scope.division_final_id].division_final_rounds[$scope.round_idx].division_final_matches;
            $scope.match =  _.filter(matches, function(o) { return o.division_final_match_id == $scope.division_final_match_id; })[0];
            
        });
        $scope.setFinalsMatchGameResult = function(finals_match_game_result,complete){
            Modals.loading();
            if(complete != undefined){
                finals_match_game_result.completed=true;
            }
            finals_match_game_result = TimeoutResources.SetFinalsMatchGameResult(undefined,{site:$scope.site},finals_match_game_result);
            finals_match_game_result.then(function(data){                
                finals_promise = TimeoutResources.GetDivisionFinals(undefined,{site:$scope.site});                
                finals_promise.then(function(data){
                    $scope.resources = TimeoutResources.GetAllResources();
                    Modals.loaded();
                    matches = $scope.resources.finals.data[$scope.division_final_id].division_final_rounds[$scope.round_idx].division_final_matches;
                    $scope.match =  _.filter(matches, function(o) { return o.division_final_match_id == $scope.division_final_match_id; })[0];                    
                });                                
            });
        };
        $scope.onScoreChange = function(score){
            score.score = score.score.replace(/\,/g,'').replace(/(\d)(?=(\d{3})+(?!\d))/g, '$1,');
        };
        
        //Modals.loading();
        // = TimeoutResources.GetEtcData();
        //.then(function(data){
        // $scope.resources = TimeoutResources.GetAllResources();
        //  Modals.loaded();
        //})
    }]
);
