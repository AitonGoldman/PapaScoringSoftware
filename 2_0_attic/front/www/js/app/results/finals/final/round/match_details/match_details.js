angular.module('app.results.finals.final.round.match_details',[/*REPLACEMECHILD*/]);
angular.module('app.results.finals.final.round.match_details').controller(
    'app.results.finals.final.round.match_details',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;
	$scope.division_final_match_idx=$state.params.division_final_match_idx;
	$scope.division_final_match_id=$state.params.division_final_match_id;
	$scope.division_final_id=$state.params.division_final_id;
	$scope.round_idx=$state.params.round_idx;
	$scope.count=$state.params.count;
        
        $scope.utils = Utils;
        Modals.loading();
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
        finals_promise = TimeoutResources.GetDivisionFinals($scope.bootstrap_promise,{site:$scope.site});        
        // = TimeoutResources.GetEtcData();
        finals_promise.then(function(data){
            $scope.resources = TimeoutResources.GetAllResources();
            Modals.loaded();
            //console.log($state.params);
            //console.log($scope.resources);
            matches = $scope.resources.finals.data[$scope.division_final_id].division_final_rounds[$scope.round_idx].division_final_matches;            
            $scope.match =  _.filter(matches, function(o) {                                
                return o.division_final_match_id == $scope.division_final_match_id;
            })[0];                        
        });
             
        //Modals.loading();
        // = TimeoutResources.GetEtcData();
        //.then(function(data){
        // $scope.resources = TimeoutResources.GetAllResources();
        //  Modals.loaded();
        //})
    }]
);
