angular.module('app.results.divisions.division',[/*REPLACEMECHILD*/]);
angular.module('app.results.divisions.division').controller(
    'app.results.divisions.division',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;
	$scope.division_id=$state.params.division_id;
	$scope.division_name=$state.params.division_name;

        $scope.utils = Utils;
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
        results_promise = TimeoutResources.GetDivisionResults(undefined,{site:$scope.site,division_id:$scope.division_id});
        Modals.loading();
        // = TimeoutResources.GetEtcData();
        results_promise.then(function(data){
            $scope.resources = TimeoutResources.GetAllResources();
            Modals.loaded();
        });
    }]
);
