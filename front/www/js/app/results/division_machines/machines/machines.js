angular.module('app.results.division_machines.machines',['app.results.division_machines.machines.machine',
    /*REPLACEMECHILD*/]);
angular.module('app.results.division_machines.machines').controller(
    'app.results.division_machines.machines',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;
	$scope.division_id=$state.params.division_id;

        $scope.utils = Utils;
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
        division_machines_promise = TimeoutResources.GetDivisionMachines($scope.bootstrap_promise,{site:$scope.site,division_id:$scope.division_id});
        Modals.loading();
        // = TimeoutResources.GetEtcData();
        division_machines_promise.then(function(data){
         $scope.resources = TimeoutResources.GetAllResources();
          Modals.loaded();
        });
    }]
);
