angular.module('app.finals_scorekeeper.division_final.match.play_order',[/*REPLACEMECHILD*/]);
angular.module('app.finals_scorekeeper.division_final.match.play_order').controller(
    'app.finals_scorekeeper.division_final.match.play_order',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;
	$scope.round_id=$state.params.round_id;
	$scope.division_final_id=$state.params.division_final_id;
	$scope.game_index=$state.params.game_index;
	$scope.match_id=$state.params.match_id;
        $scope.play_order_list = [1,2,3,4];
        $scope.resources={};
        $scope.players=undefined;

        
        $scope.disabled_play_orders = function(player_obj,play_order){                                                
            var result = undefined;
            _.forEach($scope.players, function(player) {
                if(player!=player_obj){
                    if(player.play_order==player_obj.play_order && play_order==player_obj.play_order){
                        result=true;
                    } else {                        
                    }
                } 
            });
            return result;
            // game_result = $scope.resources.scorekeeping_division_final.data.division_final_rounds[$scope.round_id-1].division_final_matches[$scope.match_id].final_match_game_results[index];                       _.forEach(game_result.division_final_match_game_player_results, function(player) {
            //     if(player!=player_obj){
            //         if(player.play_order+""!=player_obj.play_order+""){                        
            //             return true;
            //         } else {                        
            //         }
            //     } 
            // });            
            // return false;
        };
        $scope.on_submit = function(){
            game = $scope.resources.scorekeeping_division_final.data.division_final_rounds[$scope.round_id-1].division_final_matches[$scope.match_id].final_match_game_results[$scope.game_index];
            Modals.loading();
            async.waterfall([
                function(callback){                    
                    TimeoutResources.ScorekeeperRecordGameResult({site:$scope.site,division_final_match_game_result_id:game.division_final_match_game_result_id},game,callback);                    
                }],function(err,result){
                    Modals.loaded();
                    if (err == null){
                        $scope.resources[result.resource_name] = result;
                        $state.go('.^');                        
                        //$scope.resources = Utils.extract_results_from_response(result);
                    } else {
                        console.log(err);                                
                    }
                });             
        };
        $scope.utils = Utils;
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
                    //GUYH!  We have to do this sorting to match the sorting happening on the match page
                    games = $scope.resources.scorekeeping_division_final.data.division_final_rounds[$scope.round_id-1].division_final_matches[$scope.match_id].final_match_game_results;
                    games = _.sortBy(games, [function(o) { return o.division_final_match_game_result_id; }]);
                    $scope.resources.scorekeeping_division_final.data.division_final_rounds[$scope.round_id-1].division_final_matches[$scope.match_id].final_match_game_results=games;
                    $scope.players = games[$scope.game_index].division_final_match_game_player_results;
                    //$scope.resources = Utils.extract_results_from_response(result);
                } else {
                    console.log(err);                                
                }
            });  
    }]
);
