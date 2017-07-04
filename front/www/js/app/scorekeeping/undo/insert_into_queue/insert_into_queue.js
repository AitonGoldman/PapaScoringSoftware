angular.module('app.scorekeeping.undo.insert_into_queue',['app.scorekeeping.undo.insert_into_queue.player_select',
    /*REPLACEMECHILD*/]);
angular.module('app.scorekeeping.undo.insert_into_queue').controller(
    'app.scorekeeping.undo.insert_into_queue',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;
	$scope.division_id=$state.params.division_id;

        $scope.utils = Utils;
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
        Modals.loading();
        division_machines_promise = TimeoutResources.GetDivisionMachines($scope.bootstrap_promise,
                                                                         {site:$scope.site,division_id:$scope.division_id});        
        division_machines_promise.then(function(data){
            $scope.resources = TimeoutResources.GetAllResources();
            $scope.flattened_division_machines = _.values($scope.resources.division_machines.data);            
            $scope.flattened_division_machines.sort(function (a, b) {
                //return (a.division_machine_id > b.division_machine_id ? 1 : -1);
                return (a.division_machine_name > b.division_machine_name ? 1 : -1);
            });            
            Modals.loaded();
        });             

        //
        // = TimeoutResources.GetEtcData();
        //.then(function(data){
        // $scope.resources = TimeoutResources.GetAllResources();
        //  Modals.loaded();
        //})
    }]
);
