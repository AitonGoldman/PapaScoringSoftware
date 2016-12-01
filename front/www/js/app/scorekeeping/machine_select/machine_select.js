angular.module('app.scorekeeping.machine_select',['app.scorekeeping.machine_select.player_select',
    'app.scorekeeping.machine_select.record_score',
    /*REPLACEMECHILD*/]);
angular.module('app.scorekeeping.machine_select').controller(
    'app.scorekeeping.machine_select',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;
	$scope.division_id=$state.params.division_id;

        $scope.utils = Utils;
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
        division_machines_promise = TimeoutResources.GetDivisionMachines(undefined,{site:$scope.site,division_id:$scope.division_id});        
             
        Modals.loading();
        //= TimeoutResources.GetEtcData();
        division_machines_promise.then(function(data){
        $scope.resources = TimeoutResources.GetAllResources();
         Modals.loaded();
        });
    }]
);
