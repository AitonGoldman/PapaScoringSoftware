angular.module('app.finals_scorekeeper.division_final.match.resolve_tiebreaker',[/*REPLACEMECHILD*/]);
angular.module('app.finals_scorekeeper.division_final.match.resolve_tiebreaker').controller(
    'app.finals_scorekeeper.division_final.match.resolve_tiebreaker',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;
	$scope.round_id=$state.params.round_id;
	$scope.match_id=$state.params.match_id;
	$scope.division_final_id=$state.params.division_final_id;
        $scope.tiebreakers_resolved=false;
        $scope.utils = Utils;        
        $scope.resources={};
        $scope.scoreReviewed={checked:true};
        $scope.submit_tiebreaker_results = function(){
            Modals.loading();
            _.forEach($scope.match_result.final_match_player_results, function(player_result) {
                player_result.tiebreaker_score=parseInt(player_result.tiebreaker_score);
            });
                

            async.waterfall([
                function(callback){                    
                    TimeoutResources.ScorekeeperResolveTiebreaker({site:$scope.site,division_final_match_result_id:$scope.match_id},$scope.match_result,callback);
                }],function(err,result){
                    Modals.loaded();
                    if (err == null){
                        $scope.resources[result.resource_name] = result;                                        
                        console.log($scope.resources);
                        $scope.tiebreakers_resolved=true;

                        //$scope.resources = Utils.extract_results_from_response(result);
                    } else {
                        console.log(err);                                
                    }
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
                    $scope.match_result = $scope.resources.scorekeeping_division_final.data.division_final_rounds[$scope.round_id-1].division_final_matches[$scope.match_id];
                    
                    console.log($scope.resources);
                    //$scope.resources = Utils.extract_results_from_response(result);
                } else {
                    console.log(err);                                
                }
            });        
    }]
);
