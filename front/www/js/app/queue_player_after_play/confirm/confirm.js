angular.module('app.queue_player_after_play.confirm',['app.queue_player_after_play.confirm.process',
    /*REPLACEMECHILD*/]);
angular.module('app.queue_player_after_play.confirm').controller(
    'app.queue_player_after_play.confirm',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;
	$scope.division_id=$state.params.division_id;
        $scope.division_name=$state.params.division_name;
        $scope.division_machine_just_played_id=$state.params.division_machine_just_played_id;

        $scope.division_machine_to_queue_on_id=$state.params.division_machine_to_queue_on_id;
	$scope.division_machine_to_queue_on_name=$state.params.division_machine_to_queue_on_name;        
        $scope.player_name=$state.params.player_name;
	$scope.player_id=$state.params.player_id;

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
