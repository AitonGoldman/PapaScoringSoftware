angular.module('app.finals.manage.tiebreakers',['app.finals.manage.tiebreakers.resolve',
    /*REPLACEMECHILD*/]);
angular.module('app.finals.manage.tiebreakers').controller(
    'app.finals.manage.tiebreakers',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;
	$scope.division_final_id=$state.params.division_final_id;
	$scope.division_id=$state.params.division_id;
        
        $scope.utils = Utils;
        $scope.resources = {};
        
        Modals.loading();
        //$scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state); 
        thing = async.waterfall([
            function(callback){                
                TimeoutResources.GetDivisionFinalTiebreakers({site:$scope.site,division_final_id:$scope.division_final_id},undefined,callback);                    
            },
            function(result,callback){                    
                $scope.resources[result.resource_name] = result;
                if($scope.resources[result.resource_name].data.tiebreakers.length == 0){
                    callback('no tiebreakers to load',null);
                    return;
                }                    
                TimeoutResources.GetDivisionFinalImportantTiebreakerRanks({site:$scope.site,division_final_id:$scope.division_final_id},undefined,callback);
            }                                            
        ],function(err,result){
            Modals.loaded();
            if (err == null){
                $scope.resources[result.resource_name] = result;
                //$scope.important_bye_rank = $scope.resources.division_final_important_tiebreaker_ranks.data.important_tiebreakers.bye;
                $scope.important_bye_ranks = $scope.resources.division_final_important_tiebreaker_ranks.data.important_tiebreakers.bye;                
                console.log('poooooop');
                console.log($scope.resources.division_final_important_tiebreaker_ranks.data.important_tiebreakers);
                $scope.important_qualifying_rank = $scope.resources.division_final_important_tiebreaker_ranks.data.important_tiebreakers.qualifying;
                
                console.log($scope.resources);
                //$scope.resources = Utils.extract_results_from_response(result);
            } else {
                console.log(err);                                
            }
        });
        
        console.log(thing);
        //Modals.loading();
        // = TimeoutResources.GetEtcData();
        //.then(function(data){
        // $scope.resources = TimeoutResources.GetAllResources();
        //  Modals.loaded();
        //})
    }]
);
