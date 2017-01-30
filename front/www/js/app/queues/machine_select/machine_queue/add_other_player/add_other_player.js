angular.module('app.queues.machine_select.machine_queue.add_other_player',['app.queues.machine_select.machine_queue.add_other_player.process',
    /*REPLACEMECHILD*/]);
angular.module('app.queues.machine_select.machine_queue.add_other_player').controller(
    'app.queues.machine_select.machine_queue.add_other_player',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;
	$scope.division_id=$state.params.division_id;
	$scope.division_machine_name=$state.params.division_machine_name;
	$scope.division_machine_id=$state.params.division_machine_id;
	$scope.manage=$state.params.manage;

        $scope.utils = Utils;
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
             
        //Modals.loading();
        // = TimeoutResources.GetEtcData();
        //.then(function(data){
        // $scope.resources = TimeoutResources.GetAllResources();
        //  Modals.loaded();
        //})
    }]
);
