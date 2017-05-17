angular.module('app.finals.manage.tiebreakers.resolve',[/*REPLACEMECHILD*/]);
angular.module('app.finals.manage.tiebreakers.resolve').controller(
    'app.finals.manage.tiebreakers.resolve',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;
	$scope.division_final_id=$state.params.division_final_id;
	$scope.division_id=$state.params.division_id;
	$scope.rank_to_resolve=$state.params.rank_to_resolve;
        $scope.resources={};
        $scope.utils = Utils;
        $scope.scoreReviewed={checked:true};
        $scope.hideBackButton=false;
        $scope.check_tiebreaker_scores_entered = function(tiebreaker_players){            
            return _.filter(tiebreaker_players,
                            function(tiebreaker_player) { return tiebreaker_player.player_score!=undefined; }).length == tiebreaker_players.length;
        };
        $scope.submit_tiebreaker_results = function(tiebreaker_results){
            Modals.loading();
            thing = async.waterfall([
                function(callback){                
                    TimeoutResources.SubmitDivisionFinalTiebreakerResults({site:$scope.site,division_final_id:$scope.division_final_id},tiebreaker_results,callback);                    
                }                                            
            ],function(err,result){
                Modals.loaded();
                $scope.hideBackButton=true;                
                if (err == null){
                    $scope.resources[result.resource_name] = result;
                    $scope.resources.division_final_tiebreakers=undefined;
                    console.log($scope.resources);
                    //$scope.resources = Utils.extract_results_from_response(result);
                } else {
                    console.log(err);                                
                }
            });            
        };
        //$scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
        thing = async.waterfall([
            function(callback){                
                TimeoutResources.GetDivisionFinalTiebreakers({site:$scope.site,division_final_id:$scope.division_final_id},undefined,callback);                    
            }                                            
        ],function(err,result){
            Modals.loaded();
            if (err == null){
                $scope.resources[result.resource_name] = result;                
                //$scope.resources = Utils.extract_results_from_response(result);
            } else {
                console.log(err);                                
            }
        });

        
        //Modals.loading();
        // = TimeoutResources.GetEtcData();
        //.then(function(data){
        // $scope.resources = TimeoutResources.GetAllResources();
        //  Modals.loaded();
        //})
    }]
);
