angular.module('app.results.division_machines.machines.machine',[/*REPLACEMECHILD*/]);
angular.module('app.results.division_machines.machines.machine').controller(
    'app.results.division_machines.machines.machine',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;
        $scope.division_machine_id=$state.params.division_machine_id;
	$scope.division_machine_name=$state.params.division_machine_name;        
	$scope.division_id=$state.params.division_id;

        $scope.utils = Utils;
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                

        results_promise = TimeoutResources.GetDivisionMachineResults(undefined,{site:$scope.site,division_machine_id:$scope.division_machine_id});
        Modals.loading();
        // = TimeoutResources.GetEtcData();
        results_promise.then(function(data){
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
