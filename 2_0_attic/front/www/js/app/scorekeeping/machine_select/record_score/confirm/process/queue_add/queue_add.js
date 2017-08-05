angular.module('app.scorekeeping.machine_select.record_score.confirm.process.queue_add',['app.scorekeeping.machine_select.record_score.confirm.process.queue_add.process',
    /*REPLACEMECHILD*/]);
angular.module('app.scorekeeping.machine_select.record_score.confirm.process.queue_add').controller(
    'app.scorekeeping.machine_select.record_score.confirm.process.queue_add',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;
	$scope.score=$state.params.score;
	$scope.player_name=$state.params.player_name;
	$scope.division_machine_name=$state.params.division_machine_name;
	$scope.player_id=$state.params.player_id;
	$scope.division_machine_id=$state.params.division_machine_id;
	$scope.division_id=$state.params.division_id;

        $scope.utils = Utils;
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
        division_machines_promise = TimeoutResources.GetDivisionMachines(undefined,{site:$scope.site,division_id:$scope.division_id});        
//        $scope.queues = [];
        Modals.loading();
        // = TimeoutResources.GetEtcData();
        division_machines_promise.then(function(data){
            $scope.resources = TimeoutResources.GetAllResources();
            // _.forEach($scope.resources.division_machines.data, function(value, key) {
            //     if(value.player_id!=undefined){
            //         $scope.queues.push(value);
            //     }                
            // });
            Modals.loaded();
        });
    }]
);
