angular.module('app.finals_scorekeeper.division_final',['app.finals_scorekeeper.division_final.match',
    /*REPLACEMECHILD*/]);
angular.module('app.finals_scorekeeper.division_final').controller(
    'app.finals_scorekeeper.division_final',[
        '$scope','$state','TimeoutResources','Utils','Modals','$ionicHistory',
        function($scope, $state, TimeoutResources, Utils,Modals,$ionicHistory) {
            $scope.site=$state.params.site;
	    $scope.division_final_id=$state.params.division_final_id;
	    $scope.round_id=$state.params.round_id;
            
            $scope.utils = Utils;
            $scope.resources={};

            $scope.complete_round = function(){
                Modals.loading();
                async.waterfall([
                function(callback){
                    division_final_round_id = $scope.resources.scorekeeping_division_final.data.division_final_rounds[$scope.round_id-1].division_final_round_id;
                    TimeoutResources.ScorekeeperCompleteRound({site:$scope.site,division_final_match_round_id:division_final_round_id},undefined,callback);
                },                
                function(result,callback){                   
                    $scope.resources[result.resource_name] = result;                    
                    TimeoutResources.GetScorekeeperDivisionFinal({site:$scope.site,division_final_id:$scope.division_final_id},undefined,callback);
                }],function(err,result){
                Modals.loaded();
                if (err == null){
                    $scope.resources[result.resource_name] = result;                    
                    console.log($scope.resources);
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
                    console.log($scope.resources);
                    //$scope.resources = Utils.extract_results_from_response(result);
                } else {
                    console.log(err);                                
                }
            });
        }]
);


