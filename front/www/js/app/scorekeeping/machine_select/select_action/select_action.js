angular.module('app.scorekeeping.machine_select.select_action',[/*REPLACEMECHILD*/]);
angular.module('app.scorekeeping.machine_select.select_action').controller(
    'app.scorekeeping.machine_select.select_action',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;
	$scope.division_id=$state.params.division_id;
	$scope.division_machine_id=$state.params.division_machine_id;

        $scope.utils = Utils;
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                

        Modals.loading();
        queues_promise = TimeoutResources.GetQueues($scope.bootstrap_promise,{site:$scope.site,division_id:$scope.division_id});

        //division_machines_promise = TimeoutResources.GetDivisionMachines(undefined,
        //                                                                 {site:$scope.site,division_id:$scope.division_id});        
        //division_machines_promise.then(function(data){
        queues_promise.then(function(data){
            $scope.resources = TimeoutResources.GetAllResources();                
            //$scope.division_machine = $scope.resources.division_machines.data[$scope.division_machine_id];
            console.log($scope.resources);
            $scope.division_machine = $scope.resources.queues.data[$scope.division_machine_id];
            Modals.loaded();
        });
        
        $scope.goto_next_scorekeeping_step = function(division_machine_id){
            
            if($scope.resources.queues.machine_players[division_machine_id] != undefined){
                $state.go('.^.record_score',
                          {division_machine_id:$scope.division_machine.division_machine_id,
                           division_machine_name:$scope.division_machine.division_machine_name,
                           player_name:$scope.resources.queues.machine_players[division_machine_id],
                           player_id:$scope.resources.queues.data[division_machine_id].player_id,
                           team_tournament:false});
            } else {
                $state.go('.^.player_select',
                          {division_machine_id:$scope.division_machine.division_machine_id,
                           division_machine_name:$scope.division_machine.division_machine_name});                        
            }
        };
        
        
        //Modals.loading();
        // = TimeoutResources.GetEtcData();
        //.then(function(data){
        // $scope.resources = TimeoutResources.GetAllResources();
        //  Modals.loaded();
        //})
    }]
);
