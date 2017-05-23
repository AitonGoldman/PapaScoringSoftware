angular.module('app.finals_scorekeeper.division_final.match',['app.finals_scorekeeper.division_final.match.play_order',
    'app.finals_scorekeeper.division_final.match.resolve_tiebreaker',
    /*REPLACEMECHILD*/]);
angular.module('app.finals_scorekeeper.division_final.match').controller(
    'app.finals_scorekeeper.division_final.match',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;
	$scope.round_id=$state.params.round_id;
	$scope.match_id=$state.params.match_id;
	$scope.division_final_id=$state.params.division_final_id;
        $scope.resources={};
        $scope.utils = Utils;
        $scope.play_order_list = [1,2,3,4];
        $scope.onScoreChange = function(player){
            player.score = player.score.replace(/\,/g,'').replace(/(\d)(?=(\d{3})+(?!\d))/g, '$1,');
        };

        $scope.on_submit = function(game){
            //game = $scope.resources.scorekeeping_division_final.data.division_final_rounds[$scope.round_id-1].division_final_matches[$scope.match_id].final_match_game_results[game_index];
            Modals.loading();
            async.waterfall([
                function(callback){                    
                    TimeoutResources.ScorekeeperRecordGameResult({site:$scope.site,division_final_match_game_result_id:game.division_final_match_game_result_id},game,callback);                    
                },function(result,callback){
                    $scope.resources[result.resource_name] = result;                                            
                    TimeoutResources.GetScorekeeperDivisionFinal({site:$scope.site,division_final_id:$scope.division_final_id},undefined,callback);                    
                }],function(err,result){
                    Modals.loaded();
                    if (err == null){
                        $scope.resources[result.resource_name] = result;
                        $scope.reset_game_reviewed_add_scores_commas();                        
                        console.log($scope.resources);
                        //$scope.resources = Utils.extract_results_from_response(result);
                    } else {
                        console.log(err);                                
                    }
                });             
        };
        $scope.check_if_machine_player_order_set = function(game){                        
            if(game.division_machine_string!=undefined && game.division_final_match_game_player_results[0].play_order!=undefined){
                return false;
             }
            return true;
        };
        $scope.disabled_play_orders = function(index,play_order){            
            game_results = $scope.resources.scorekeeping_division_final.data.division_final_rounds[$scope.round_id-1].division_final_matches[$scope.match_id].final_match_game_results[index];
            for (player in game_results.division_final_match_game_player_results){
                if(game_results.division_final_match_game_player_results[player].play_order==play_order){
                    return true;
                };    
            }
            return false;
        };
        $scope.on_play_order_change = function(index){            
            game_results = $scope.resources.scorekeeping_division_final.data.division_final_rounds[$scope.round_id-1].division_final_matches[$scope.match_id].final_match_game_results[index];
            console.log(game_results);
            for (player in game_results.division_final_match_game_player_results){
                console.log(game_results.division_final_match_game_player_results[player]);    
            }
            
        };
        $scope.reset_game_reviewed_add_scores_commas = function(){
            games = $scope.resources.scorekeeping_division_final.data.division_final_rounds[$scope.round_id-1].division_final_matches[$scope.match_id].final_match_game_results;
            _.forEach(games, function(game) {
                game.reviewed=true;
                _.forEach(game.division_final_match_game_player_results, function(player) {
                    if(player.score != null){
                        player.score=""+player.score;
                        $scope.onScoreChange(player);
                    }                            
                });                                 
            });
        };
        Modals.loading();
        async.waterfall([
            function(callback){                    
                TimeoutResources.GetDivisionFinals({site:$scope.site},undefined,callback);
            },                
            function(result,callback){                   
                $scope.resources[result.resource_name] = result;                    
                TimeoutResources.GetScorekeeperDivisionFinal({site:$scope.site,division_final_id:$scope.division_final_id},undefined,callback);
            }],function(err,result){
                Modals.loaded();
                if (err == null){
                    $scope.resources[result.resource_name] = result;
                    // games = $scope.resources.scorekeeping_division_final.data.division_final_rounds[$scope.round_id-1].division_final_matches[$scope.match_id].final_match_game_results;
                    // _.forEach(games, function(game) {
                    //     game.reviewed=true;
                    //     _.forEach(game.division_final_match_game_player_results, function(player) {
                    //         if(player.score != null){
                    //             player.score=""+player.score;
                    //             $scope.onScoreChange(player);
                    //         }                            
                    //     });                                 
                    // });
                    $scope.reset_game_reviewed_add_scores_commas();                    
                    console.log($scope.resources);
                    //$scope.resources = Utils.extract_results_from_response(result);
                } else {
                    console.log(err);                                
                }
            });        
    }]
);
