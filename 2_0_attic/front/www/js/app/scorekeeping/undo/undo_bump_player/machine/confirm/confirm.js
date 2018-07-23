angular.module('app.scorekeeping.undo.undo_bump_player.confirm',['app.scorekeeping.undo.undo_bump_player.confirm.process',
    /*REPLACEMECHILD*/]);
angular.module('app.scorekeeping.undo.undo_bump_player.confirm').controller(
    'app.scorekeeping.undo.undo_bump_player.confirm',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;
	$scope.division_machine_id=$state.params.division_machine_id;
	$scope.division_machine_name=$state.params.division_machine_name;

	$scope.division_id=$state.params.division_id;

        $scope.utils = Utils;
        Modals.loading();
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
        queues_promise = TimeoutResources.GetQueues($scope.bootstrap_promise,{site:$scope.site,division_id:$scope.division_id});
        queues_promise.then(function(data){
            $scope.resources = TimeoutResources.GetAllResources();
            if($scope.resources.queues.data[$scope.division_machine_id].queues.length < 2){
                Modals.loaded();
                return;
            }
            $scope.player_id=$scope.resources.queues.data[$scope.division_machine_id].queues[1].player.player_id;
            $scope.player_name=$scope.resources.queues.data[$scope.division_machine_id].queues[1].player.player_name;
            console.log($scope.resources.queues.data[$scope.division_machine_id].queues[1].player);
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
