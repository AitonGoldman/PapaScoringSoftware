angular.module('app.results.finals.final.round',['app.results.finals.final.round.match_details',
    /*REPLACEMECHILD*/]);
angular.module('app.results.finals.final.round').controller(
    'app.results.finals.final.round',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;
	$scope.round_idx=$state.params.round_idx;
	$scope.count=$state.params.count;
	$scope.division_final_id=$state.params.division_final_id;

        $scope.utils = Utils;
        Modals.loading();
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
        finals_promise = TimeoutResources.GetDivisionFinals(undefined,{site:$scope.site});                
        finals_promise.then(function(data){
            $scope.resources = TimeoutResources.GetAllResources();            
            Modals.loaded();                                        
        });                                                
             
        //Modals.loading();
        // = TimeoutResources.GetEtcData();
        //.then(function(data){
        // $scope.resources = TimeoutResources.GetAllResources();
        //  Modals.loaded();
        //})
    }]
);
