angular.module('app.scorekeeping.machine_select.record_score.confirm.process.queue_add.process',[/*REPLACEMECHILD*/]);
angular.module('app.scorekeeping.machine_select.record_score.confirm.process.queue_add.process').controller(
    'app.scorekeeping.machine_select.record_score.confirm.process.queue_add.process',[
    '$scope','$state','TimeoutResources','Utils','Modals',
    function($scope, $state, TimeoutResources, Utils,Modals) {
        $scope.site=$state.params.site;
	$scope.division_id=$state.params.division_id;
	$scope.score=$state.params.score;
	$scope.player_name=$state.params.player_name;
	$scope.division_machine_name=$state.params.division_machine_name;
	$scope.division_machine_id=$state.params.division_machine_id;
	$scope.player_id=$state.params.player_id;
	$scope.queued_division_machine_name=$state.params.queued_division_machine_name;
	$scope.queued_division_machine_id=$state.params.queued_division_machine_id;
        
        $scope.utils = Utils;
        $scope.bootstrap_promise = $scope.controller_bootstrap($scope,$state);                
         $scope.process_step=$state.params.process_step;
        if(_.size($scope.process_step)==0){
            //Utils.stop_post_reload();
            Modals.error('Tried to reload a page that submits data.',$scope.site,'app');
            return;
        }
        
        add_to_queue_promise = TimeoutResources.AddToQueue(undefined,{site:$scope.site},{division_machine_id:$scope.queued_division_machine_id,player_id:$scope.player_id});
        Modals.loading();
        // = TimeoutResources.GetEtcData();
        add_to_queue_promise.then(function(data){
         $scope.resources = TimeoutResources.GetAllResources();
          Modals.loaded();
        });
    }]
);
